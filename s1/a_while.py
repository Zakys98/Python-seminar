# Implement an interpreter for simple ‘while programs’ (so called
# because their only looping construct is ‹while›). The syntax is as
# follows:
#
#  • one line = one statement (no exceptions),
#  • the program is a sequence of statements,
#  • blocks are delimited by indentation (1–5 spaces),
#  • there are following statement types:
#    ◦ assignment,
#    ◦ ‹if› statement,
#    ◦ ‹while› statement.
#
# All variables are global and do not need to be declared (they come
# into existence when they are first used, with a default value 0).
# Variables are always integers. Variable names start with a letter
# and may contain letters, underscores and digits.
#
# The ‹if› and ‹while› statements are followed by a «body»: a block
# indented one space beyond the ‹if› or ‹while› itself. The body
# might be empty. The ‹if› and ‹while› keywords are followed by a
# single variable name. Zero means false, anything else means true.
#
# Assignments are of two forms:
#
#  • constant assignments of the form ‹name = number› (where
#    ‹number› is an integer written in decimal, and might be
#    negative),
#  • 3-address code operations, of the form
#
#        name₀ = operation name₁ name₂
#
# Valid operations are:
#
#  • logic: ‹and›, ‹or›, ‹nand› (the result is always 0 or 1),
#  • arithmetic: ‹add›, ‹sub›, ‹mul›, ‹div›,
#  • relational:
#    ◦ ‹lt›, ‹gt› (less/greater than),
#    ◦ ‹eq› (equals),
#    ◦ ‹leq› and ‹geq› (less/greater or equal).
#
# Example program:
#
#     x = 0
#     y = 7
#     one = 1
#     if x
#      x = add x x
#     while y
#      y = sub y one
#      x = add x one
#
# Write a function ‹do_while› which takes a ‘while program’ (as a
# string) and returns a dictionary with variable names as keys and
# their final values as values (of type ‹int›).
#
# If the program contains an error, create a special variable named
# ‹#error› and set its value to the offending line number. Return
# immediately after encountering the error. In this case, other
# variables may or may not be included in the resulting dictionary.
#
# Check syntax before you start executing the program (i.e. the
# following program should return an error on line 3 and should
# «not» loop forever):
#
#     x = 1
#     while x
#     x ++
#
# Syntax errors may be due to malformed statements (e.g. ‹while x =
# 1›, ‹x ++› above, etc.), or due to undefined operations (e.g. ‹x =
# mod x y›). Report the first error (nearest to the top of the
# input). At runtime, detect and report any attempts to divide by
# zero.

from typing import Callable
import re

from rx import catch


class GlobalContext:
    globalVariables: dict[str, int] = {}


class Helpers:
    @staticmethod
    def getStrIndentation(string: str) -> int:
        # TODO if there is tab, throw error
        return len(string) - len(string.lstrip())

    @staticmethod
    def checkVarName(name: str) -> bool:
        location = re.search("^$", name)  # TODO not finished
        if location == None:
            return False
        return True

    @staticmethod
    def set_error(whichLine: int) -> None:
        GlobalContext.globalVariables["#error"] = whichLine + 1


variableRegex = "[a-zA-Z][a-zA-Z0-9_]*"
operationsRegex = "add|sub|mul|div|and|or|nand|lt|gt|eq|leq|geq"


class Program:
    def __init__(self, sourceCode: str) -> None:
        self.sourceLines = sourceCode.splitlines()
        self.actual_line = 0

    def create(self) -> None:
        while self.actual_line < len(self.sourceLines):
            cmd = self.sourceLines[self.actual_line].strip().split(' ')[0]
            if cmd == 'if':
                if_cmd = IfCommand()
                self.actual_line = if_cmd.parse(
                    self.sourceLines, self.actual_line)
            elif cmd == 'while':
                pass
            else:
                ass_cmd = AssignmentCommand()
                self.actual_line = ass_cmd.parse(
                    self.sourceLines, self.actual_line)

    def run(self) -> None:
        pass


class Command:
    def run(self) -> None:
        pass


class WhileCommand(Command):
    pass


class IfCommand(Command):
    conditionVar = ""
    commandsBlock = None

    #def run(self) -> None:
    #    if(GlobalContext.globalVariables[self.conditionVar] != 0):
    #       self.commandsBlock.run()

    def parse(self, sourceLines: list[str], lineNumber: int) -> int:
        cmd = sourceLines[lineNumber]
        regexPattern = f"\s*if ({variableRegex})\s*$"
        regexResult = re.match(regexPattern, cmd)
        if regexResult is None:
            Helpers.set_error(lineNumber)
            raise RuntimeError('Not a condition format.')
        self.conditionVar = regexResult.group(1)
        # tenhle if tady asi nebude, kazda variable ma na zacatku 0
        if self.conditionVar not in GlobalContext.globalVariables:
            Helpers.set_error(lineNumber)
            raise RuntimeError('Variable does not exist.')
        self.commandsBlock = BlockOfCommands()
        nextLine = self.commandsBlock.parseBlock(sourceLines, lineNumber + 1)

        return nextLine


class AssignmentCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        self.assignmentLambda: dict[str, Callable[[str, str], int]] = {
            'add': lambda first, second: GlobalContext.globalVariables[first] + GlobalContext.globalVariables[second],
            'sub': lambda first, second: GlobalContext.globalVariables[first] - GlobalContext.globalVariables[second],
            'mul': lambda first, second: GlobalContext.globalVariables[first] * GlobalContext.globalVariables[second],
            'div': lambda first, second: GlobalContext.globalVariables[first] // GlobalContext.globalVariables[second],
            'and': lambda first, second: GlobalContext.globalVariables[first] and GlobalContext.globalVariables[second],
            'or': lambda first, second: GlobalContext.globalVariables[first] or GlobalContext.globalVariables[second],
            'nand': lambda first, second: not(GlobalContext.globalVariables[first] and GlobalContext.globalVariables[second]),
            'lt': lambda first, second: GlobalContext.globalVariables[first] < GlobalContext.globalVariables[second],
            'gt': lambda first, second: GlobalContext.globalVariables[first] > GlobalContext.globalVariables[second],
            'eq': lambda first, second: GlobalContext.globalVariables[first] == GlobalContext.globalVariables[second],
            'leq': lambda first, second: GlobalContext.globalVariables[first] <= GlobalContext.globalVariables[second],
            'geq': lambda first, second: GlobalContext.globalVariables[first] >= GlobalContext.globalVariables[second]
        }

    # def run(self) -> None:
    #    GlobalContext.globalVariables[self.where_save] = self.assignmentLambda()

    def parse(self, sourceLines: list[str], lineNumber: int) -> int:
        cmd = sourceLines[lineNumber]
        regexPattern1 = f"^\s*({variableRegex}) = (-?\d+)\s*$"
        regexResult1 = re.match(regexPattern1, cmd)
        if regexResult1 is not None:
            self.where_save = regexResult1.group(1)
            varValue = regexResult1.group(2)
            GlobalContext.globalVariables[self.where_save] = int(varValue)
            return lineNumber + 1
        # x = add y z
        # TODO select which operations allowed
        regexPattern2 = f"^\s*({variableRegex}) = ({operationsRegex}) ({variableRegex}) ({variableRegex})\s*$"
        regexResult2 = re.match(regexPattern2, cmd)
        if regexResult2 is not None:
            self.where_save = regexResult2.group(1)
            operation = regexResult2.group(2)
            firstOperand = regexResult2.group(3)
            secondOperand = regexResult2.group(4)
            GlobalContext.globalVariables[self.where_save] = self.assignmentLambda[operation](
                firstOperand, secondOperand)
            # else:
            #    Helpers.throwError("Bad operation", lineNumber)
            return lineNumber + 1
        Helpers.set_error(lineNumber)
        raise RuntimeError('Not assignment.')


class BlockOfCommands:
    def __init__(self) -> None:
        self.cmdsList: list[Command] = []

    def run(self) -> None:
        for i in range(0, len(self.cmdsList)):
            self.cmdsList[i].run()

    def parseBlock(self, sourceLines: list[str], lineNumber: int) -> int:
        blockIndentation = Helpers.getStrIndentation(sourceLines[lineNumber])
        while lineNumber < len(sourceLines) and Helpers.getStrIndentation(sourceLines[lineNumber]) == blockIndentation:
            assCmd = AssignmentCommand()
            nextLine = assCmd.parse(sourceLines, lineNumber)
            if nextLine is not None:
                self.cmdsList.append(assCmd)
                lineNumber = nextLine
                continue
            ifCmd = IfCommand()
            nextLine = ifCmd.parse()
            if nextLine is not None:
                self.cmdsList.append(ifCmd)
                lineNumber = nextLine
                continue
        return lineNumber


def do_while(source: str) -> dict[str, int]:
    program = Program(source)
    try:
        program.create()
    except RuntimeError:
        pass
    program.run()
    return GlobalContext.globalVariables


if __name__ == '__main__':
    programSource = """x = -5
    y = 7
    one = 1
    y = sub x one
    if x
      x = add x x
        if x
          x = add x x"""
    print(do_while(programSource))
