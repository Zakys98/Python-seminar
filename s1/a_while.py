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

import re

class GlobalContext():
	globalVariables = {}



class Helpers():
	@staticmethod
	def getStrIndentation(string : str):
		return len(string) - len(string.lstrip()) # TODO if there is tab, throw error

	@staticmethod
	def checkVarName(name :str):
		location = re.search("^$", name) #TODO not finished
		if location == None:
			return False
		return True

	@staticmethod
	def throwError(what, whichLine):
		GlobalContext.globalVariables["#error"] = whichLine
		raise RuntimeError(what)



variableRegex="[a-zA-Z][a-zA-Z0-9_]*"
operationsRegex="add|sub|mul|div|and|or|nand|lt|gt|eq|leq|geq"


class Program():
	def __init__(self, sourceCode) -> None:
		self.sourceCode = sourceCode
		self.sourceLines = sourceCode.splitlines()
		ass = AssignmentCommand()
		ass.parse(self.sourceLines, 0)
		ass.run()

	def create(self):
		pass

	def run(self):
		pass

class Command():
	def run(self):
		pass

class WhileCommand(Command):
	pass

class IfCommand(Command):
	conditionVar = ""
	commandsBlock = None

	def run (self):
		if(GlobalContext.globalVariables[self.conditionVar] != 0):
			self.commandsBlock.run()

	def parse(self,sourceLines, lineNumber):
		cmd = sourceLines[lineNumber]
		regexPattern = f"\s*if ({variableRegex})\s*$"
		regexResult = re.match(regexPattern, cmd)
		if(regexResult == None):
			return Helpers.throwError("Not a condition format.", lineNumber)
		self.conditionVar = regexResult.group(1)

		self.commandsBlock = BlockOfCommands()
		nextLine = self.commandsBlock.parseBlock(sourceLines, lineNumber +1)

		return nextLine







class AssignmentCommand(Command):

	varName = ""

	def run(self):
		GlobalContext.globalVariables[self.varName] = self.assignmentLambda()


	def parse(self, sourceLines, lineNumber):
		cmd = sourceLines[lineNumber]
		#x = 6
		regexPattern1 = "^\s*({var}) = (\d+)\s*$".format(var=variableRegex)
		regexResult1 = re.match(regexPattern1, cmd)
		#TODO numbers can be negative!
		if(regexResult1 != None):
			varName = regexResult1.group(1)
			varValue = regexResult1.group(2)
			self.varName = varName
			self.assignmentLambda = lambda: int(varValue)
			return lineNumber + 1
		#x = add y z
		regexPattern2 = "^\s*({var}) = ({operation}) ({var}) ({var})\s*$".format(var=variableRegex, operation=operationsRegex) # TODO select which operations allowed
		regexResult2 = re.match(regexPattern2, cmd)
		if(regexResult2 != None):
			whereSave = regexResult2.group(1)
			self.whereSave = regexResult2.group(1)
			operation = regexResult2.group(2)
			firstOperand = regexResult2.group(3)
			secondOperand = regexResult2.group(4)
			if(operation == "add"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] + GlobalContext.globalVariables[secondOperand]
			elif(operation == "sub"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] - GlobalContext.globalVariables[secondOperand]
			elif(operation == "mul"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] * GlobalContext.globalVariables[secondOperand]
			elif(operation == "div"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] // GlobalContext.globalVariables[secondOperand]
			elif(operation == "and"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] and GlobalContext.globalVariables[secondOperand]
			elif(operation == "or"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] or GlobalContext.globalVariables[secondOperand]
			elif(operation == "nand"):
				self.assignmentLambda = lambda: not (GlobalContext.globalVariables[firstOperand] and GlobalContext.globalVariables[secondOperand])
			elif(operation == "lt"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] < GlobalContext.globalVariables[secondOperand]
			elif(operation == "gt"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] > GlobalContext.globalVariables[secondOperand]
			elif(operation == "eq"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] == GlobalContext.globalVariables[secondOperand]
			elif(operation == "leq"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] <= GlobalContext.globalVariables[secondOperand]
			elif(operation == "geq"):
				self.assignmentLambda = lambda: GlobalContext.globalVariables[firstOperand] >= GlobalContext.globalVariables[secondOperand]
			else:
				Helpers.throwError("Bad operation", lineNumber)
			return lineNumber + 1
		else:
			Helpers.throwError("Not assignment.", lineNumber)

class BlockOfCommands():
	cmdsList = []
	def __init__(self) -> None:
		pass

	def run(self):
		for i in range(0, len(self.cmdsList)):
			self.cmdsList[i].run()

	def parseBlock(self, sourceLines, lineNumber):
		self.blockIndentation = Helpers.getStrIndentation(sourceLines[lineNumber])
		while(Helpers.getStrIndentation(sourceLines[lineNumber]) == self.blockIndentation):
			assCmd = AssignmentCommand()
			nextLine = assCmd.parse()
			if(nextLine != None):
				self.cmdsList.append(assCmd)
				lineNumber = nextLine
				continue
			ifCmd = IfCommand()
			nextLine = ifCmd.parse()
			if(nextLine != None):
				self.cmdsList.append(ifCmd)
				lineNumber = nextLine
				continue
			return None


def do_while(programSource):
	program = Program(programSource)
	program.create()
	return program.run();

programSrc = """x = 5"""
do_while(programSrc)
