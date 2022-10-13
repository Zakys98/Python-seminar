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
#  • relational (result is again ‹0› or ‹1›):
#    ◦ ‹lt›, ‹gt› (less/greater than),
#    ◦ ‹eq› (equals),
#    ◦ ‹leq› and ‹geq› (less/greater or equal),
#  • arithmetic: ‹add›, ‹sub›, ‹mul›, ‹div›, ‹mod›.
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
# fdiv x y›). Report the first error (nearest to the top of the
# input). At runtime, detect and report any attempts to divide by
# zero.


from typing import Callable
import re


class GlobalContext:
    globalVariables: dict[str, int] = {}

    @staticmethod
    def check_variable_exits(variable: str) -> None:
        if variable not in GlobalContext.globalVariables:
            GlobalContext.globalVariables[variable] = 0

    @staticmethod
    def set_error(whichLine: int) -> None:
        GlobalContext.globalVariables["#error"] = whichLine + 1


def get_indentation(string: str) -> int:
    # TODO if there is tab, throw error
    return len(string) - len(string.lstrip())


variableRegex = "[a-zA-Z][a-zA-Z0-9_]*"
operationsRegex = "add|sub|mul|div|mod|and|or|nand|lt|gt|eq|leq|geq"


class Program:
    def __init__(self, source_code: str) -> None:
        self.source_lines = source_code.splitlines()
        self.actual_line = 0

    def run(self) -> None:
        while self.actual_line < len(self.source_lines):
            cmd = self.source_lines[self.actual_line].strip().split(' ')[0]
            if cmd == 'if':
                if_cmd = IfCommand()
                self.actual_line = if_cmd.parse(
                    self.source_lines, self.actual_line)
            elif cmd == 'while':
                while_cmd = WhileCommand()
                self.actual_line = while_cmd.parse(
                    self.source_lines, self.actual_line)
            else:
                ass_cmd = AssignmentCommand()
                self.actual_line = ass_cmd.parse(
                    self.source_lines[self.actual_line], self.actual_line)


class Command:
    def run(self) -> None:
        pass

    def skip_lines(self, source_lines: list[str], actual_line: int) -> int:
        indentation = get_indentation(source_lines[actual_line])
        actual_line += 1
        while True:
            if actual_line >= len(source_lines):
                return actual_line
            if indentation >= get_indentation(source_lines[actual_line]):
                return actual_line
            actual_line += 1


class WhileCommand(Command):

    def parse(self, source_lines: list[str], line_number: int) -> int:
        cmd = source_lines[line_number]
        pattern = f"\s*while ({variableRegex})\s*$"
        reg_result = re.match(pattern, cmd)
        if reg_result is None:  # just for mypy
            GlobalContext.set_error(line_number)
            raise RuntimeError
        while_variable = reg_result.group(1)
        GlobalContext.check_variable_exits(while_variable)

        while_line = line_number
        indentation = get_indentation(source_lines[line_number])
        number_of_lines = len(source_lines)
        while GlobalContext.globalVariables[while_variable] != 0:
            line_number += 1
            while line_number < number_of_lines and indentation < get_indentation(source_lines[line_number]):
                cmd = source_lines[line_number].strip().split(' ')[0]
                if cmd == 'if':
                    if_cmd = IfCommand()
                    line_number = if_cmd.parse(
                        source_lines, line_number)
                elif cmd == 'while':
                    while_cmd = WhileCommand()
                    line_number = while_cmd.parse(
                        source_lines, line_number)
                else:
                    ass_cmd = AssignmentCommand()
                    line_number = ass_cmd.parse(
                        source_lines[line_number], line_number)
            line_number = while_line
        return super().skip_lines(source_lines, line_number)


class IfCommand(Command):

    def parse(self, source_lines: list[str], actual_line: int) -> int:
        pattern = f"\s*if ({variableRegex})\s*$"
        reg_result = re.match(pattern, source_lines[actual_line])
        if reg_result is None:  # just for mypy
            GlobalContext.set_error(actual_line)
            raise RuntimeError
        variable = reg_result.group(1)
        GlobalContext.check_variable_exits(variable)
        if GlobalContext.globalVariables[variable] == 0:
            return super().skip_lines(source_lines, actual_line)
        return actual_line + 1


class AssignmentCommand(Command):

    def __init__(self) -> None:
        super().__init__()
        self.assignment_function: dict[str, Callable[[str, str], int]] = {
            'add': lambda first, second: GlobalContext.globalVariables[first] + GlobalContext.globalVariables[second],
            'sub': lambda first, second: GlobalContext.globalVariables[first] - GlobalContext.globalVariables[second],
            'mul': lambda first, second: GlobalContext.globalVariables[first] * GlobalContext.globalVariables[second],
            'div': lambda first, second: GlobalContext.globalVariables[first] // GlobalContext.globalVariables[second],
            'mod': lambda first, second: GlobalContext.globalVariables[first] % GlobalContext.globalVariables[second],
            'and': lambda first, second: int(bool(GlobalContext.globalVariables[first] and GlobalContext.globalVariables[second])),
            'or': lambda first, second: int(bool(GlobalContext.globalVariables[first] or GlobalContext.globalVariables[second])),
            'nand': lambda first, second: int(bool(not(GlobalContext.globalVariables[first] and GlobalContext.globalVariables[second]))),
            'lt': lambda first, second: int(GlobalContext.globalVariables[first] < GlobalContext.globalVariables[second]),
            'gt': lambda first, second: int(GlobalContext.globalVariables[first] > GlobalContext.globalVariables[second]),
            'eq': lambda first, second: int(GlobalContext.globalVariables[first] == GlobalContext.globalVariables[second]),
            'leq': lambda first, second: int(GlobalContext.globalVariables[first] <= GlobalContext.globalVariables[second]),
            'geq': lambda first, second: int(GlobalContext.globalVariables[first] >= GlobalContext.globalVariables[second])
        }

    def parse(self, command: str, actual_line: int) -> int:
        pattern = f"^\s*({variableRegex}) = (-?\d+)\s*$"
        reg_result = re.match(pattern, command)
        if reg_result is not None:
            where_save = reg_result.group(1)
            varValue = reg_result.group(2)
            GlobalContext.globalVariables[where_save] = int(varValue)
            return actual_line + 1

        pattern = f"^\s*({variableRegex}) = ({operationsRegex}) ({variableRegex}) ({variableRegex})\s*$"
        reg_result = re.match(pattern, command)
        if reg_result is not None:
            where_save = reg_result.group(1)
            operation = reg_result.group(2)
            firstOperand = reg_result.group(3)
            secondOperand = reg_result.group(4)
            GlobalContext.check_variable_exits(firstOperand)
            GlobalContext.check_variable_exits(secondOperand)
            if (operation == 'div' or operation == 'mod') and GlobalContext.globalVariables[secondOperand] == 0:
                GlobalContext.set_error(actual_line)
                raise RuntimeError
            GlobalContext.globalVariables[where_save] = self.assignment_function[operation](
                firstOperand, secondOperand)
        return actual_line + 1


class Syntax:
    def __init__(self, source_code: str) -> None:
        self.source_lines = source_code.splitlines()
        self.actual_line = 0
        self.starting_indentation = get_indentation(
            self.source_lines[self.actual_line])
        self.actual_indentation = self.starting_indentation

    def check(self) -> None:
        while self.actual_line < len(self.source_lines):
            self._check_indentation()
            cmd = self.source_lines[self.actual_line].strip().split(' ')[0]
            if cmd == 'if':
                self._check_if()
            elif cmd == 'while':
                self._check_while()
            else:
                self._check_asignment()
            self.actual_line += 1

    def _check_indentation(self) -> None:
        indentation = get_indentation(self.source_lines[self.actual_line])
        if indentation > self.actual_indentation or indentation < self.starting_indentation:
            GlobalContext.set_error(self.actual_line)
            raise RuntimeError
        elif indentation < self.actual_indentation:
            self.actual_indentation = indentation

    def _check_line(self, pattern: str) -> None:
        regexResult = re.match(pattern, self.source_lines[self.actual_line])
        if regexResult is None:
            GlobalContext.set_error(self.actual_line)
            raise RuntimeError
        self.actual_indentation += 1

    def _check_if(self) -> None:
        self._check_line(f"\s*if ({variableRegex})\s*$")

    def _check_while(self) -> None:
        self._check_line(f"\s*while ({variableRegex})\s*$")

    def _check_asignment(self) -> None:
        cmd = self.source_lines[self.actual_line]
        regexPattern1 = f"^\s*({variableRegex}) = (-?\d+)\s*$"
        regexResult1 = re.match(regexPattern1, cmd)
        if regexResult1 is not None:
            return
        regexPattern2 = f"^\s*({variableRegex}) = ({operationsRegex}) ({variableRegex}) ({variableRegex})\s*$"
        regexResult2 = re.match(regexPattern2, cmd)
        if regexResult2 is not None:
            return
        GlobalContext.set_error(self.actual_line)
        raise RuntimeError


def do_while(source: str) -> dict[str, int]:
    GlobalContext.globalVariables.clear()
    syntax = Syntax(source)
    program = Program(source)
    try:
        syntax.check()
        program.run()
    except RuntimeError:
        pass
    return GlobalContext.globalVariables


if __name__ == '__main__':
    programSource = """x = -5
y = 7
one = 1
y = sub x one
r = sub xe po
if x
 x = add x x
 if x
  x = add x x
z = 2"""

    a = """a = 5
b = 1
x = add x x
if a
 a = 0
while x
 if x
  e = 2
  s = 2
  x = add x x
 t = 0"""
    b = """x = 1
while x
x ++"""
    c = """   x = 1
   c = 0
   if x
    a = 4
    l = 1
    if c
   q = 2"""
    d = """a = 2
one = 1
z = 0
while a
 a = sub a one
 if one
  a = 0
c = 4
"""
    e = """  a = 5
  b = 3
  c = mod a b
  zero = 0
  if zero
  d = 4"""
    l = """  x = add x x"""
    s = """ x = 2
 z = add x y"""
    print(do_while(s))
    print(do_while(l))
