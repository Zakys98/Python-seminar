# Implement an interpreter for simple recursive programs. The
# following syntax is taken unchanged from ‹s1/a_while›:
#
#  • one line = one statement (no exceptions),
#  • blocks are delimited by indentation (1–5 spaces),
#  • there are following statement types:
#    ◦ assignment,
#    ◦ ‹if› statement.
#
# There are also two important changes:
#
#  1. The right-hand side of an assignment can be a function call, in
#     addition to a built-in operation, written as:
#
#         name₀ = func name₁ name₂ … nameₙ
#
#  2. There is a new statement type, «function definition», which can
#     only appear in the top-level scope (and is the only statement
#     than can appear there), of the form:
#
#         def funcname name₁ name₂ … nameₙ
#
#     All functions can call all other functions, regardless of the
#     order in which they are defined in the source. Function names
#     follow the same rules as variable names.
#
# Semantics change in the following way:
#
#  • all variables are «local» to the function in which they are
#    used (declarations are still not needed),
#  • the result of a function call is the value of a variable with
#    the same name, i.e. in function ‹foo›, the statement ‹foo = 7›
#    sets the return value to ‹7› (but does «not» terminate the
#    function),
#  • the namespaces for variables and for functions are separate;
#    operation names (‹add›, ‹and›, …) «must not» be used for
#    functions (but they can be used for variables).
#
# Like ‹if›, a ‹def› statement is followed by a body, indented by a
# single space. Other restrictions on blocks remain the same as in
# ‹s1/a_while›.
#
# Example program:
#
#     def fib n
#      one = 1
#      two = 2
#      fib = 1
#      rec = gt n two
#      if rec
#       n_1 = sub n one
#       n_2 = sub n two
#       fib_1 = fib n_1
#       fib_2 = fib n_2
#       fib = add fib_1 fib_2
#
# Write a function ‹do_rec› which takes a recursive program (as a
# string), a function name, and an arbitrary number of integers. The
# result is the return value of the function invoked, or a tuple of
# (line number, error string) in case the program fails. Return the
# first error in this order (within a group, return the number of
# the first line with an error):
#
#  1. syntax errors (including attempts to redefine a function),
#  2. errors in function calls:
#     ◦ use of an undefined function or
#     ◦ mismatch in the number of arguments,
#  3. runtime errors (division by zero).
#
# Errors of type 2 should be reported even if they are in unused
# code (i.e. the test must be static). If the function passed to
# ‹do_rec› does not exist or the number of arguments does not match,
# return an error on (virtual) line 0.

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
    s = """x = -5
y = 7
one = 1
y = sub x one
r = sub xe po
if x
 x = add x x
 if x
  x = add x x
z = 2"""
    print(do_while(s))
