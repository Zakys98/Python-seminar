# In the first exercise, we will implement a simple RPN (Reverse
# Polish Notation) evaluator.

# The only argument the evaluator takes is a list with two kinds of
# objects in it: numbers (of type ‹int›, ‹float›, or similar) and
# operators (for simplicity, these will be of type ‹str›).  To
# evaluate an RPN expression, we will need a stack (which can be
# represented using a ‹list›, which has useful ‹append› and ‹pop›
# methods).

# Implement the following unary operators: ‹neg› (for negation, i.e.
# unary minus) and ‹recip› (for reciprocal, i.e. the multiplicative
# inverse). The entry point will be a single function, with the
# following prototype:

def rpn_unary(rpn):
    list_of_values = []
    index = -1
    for value in rpn:
        if value == "neg":
            list_of_values[index] = -list_of_values[index]
        elif value == "recip":
            list_of_values[index] = list_of_values[index] ** -1
        else:
            list_of_values.append(value)
            index += 1
    return list_of_values

# The second part of the exercise is now quite simple: extend the
# ‹rpn_unary› evaluator with the following binary operators: ‹+›,
# ‹-›, ‹*›, ‹/›, ‹**› and two ‘greedy’ operators, ‹sum› and ‹prod›,
# which reduce the entire content of the stack to a single number.
# Think about how to share code between the two evaluators.

# Note that we write the stack with ‘top’ to the right, and
# operators take arguments from left to right in this ordering (i.e.
# the top of the stack is the right argument of binary operators).
# This is important for non-commutative operators.


def rpn_binary(rpn):
    stack = []
    index = -1
    for value in rpn:
        if value == "+":
            stack.append(stack.pop() + stack.pop())
            index -= 1
        elif value == "*":
            stack.append(stack.pop() * stack.pop())
            index -= 1
        elif value == "/":
            second = stack.pop()
            first = stack.pop()
            stack.append(first / second)
            index -= 1
        elif value == "-":
            second = stack.pop()
            first = stack.pop()
            stack.append(first - second)
            index -= 1
        elif value == "**":
            second = stack.pop()
            first = stack.pop()
            stack.append(first ** second)
            index -= 1
        elif value == "neg":
            stack[index] = -stack[index]
        elif value == "recip":
            stack[index] = stack[index] ** -1
        elif value == "sum":
            number = 0
            for val in stack:
                number += val
            stack.clear()
            stack.append(number)
        elif value == "prod":
            for i in range(1, len(stack)):
                stack[0] *= stack[i]
            number = stack[0]
            stack.clear()
            stack.append(number)
        else:
            stack.append(value)
            index += 1
    return stack

# Some test cases are included below. Write a few more to convince
# yourself that your code works correctly.


def test_unary():
    rpn_num = [5]
    assert rpn_unary(rpn_num) == [5]

    rpn_neg = [1, "neg"]
    assert rpn_unary(rpn_neg) == [-1]

    rpn_rec = [2, "recip"]
    assert rpn_unary(rpn_rec) == [1/2]

    rpn_n = [-1/7, "recip"]
    assert rpn_unary(rpn_n) == [-7]

    rpn_simp = [1, "recip", "neg"]
    assert rpn_unary(rpn_simp) == [-1]

    rpn = [4, "neg", "recip", "neg", "neg", "recip", "neg",
           "recip", "recip"]
    assert rpn_unary(rpn) == [4]

    rpn_nums = [5, 1/9, "recip", 2, "neg", "recip", -1, "neg"]
    assert rpn_unary(rpn_nums) == [5, 9, -1/2, 1]


def test_binary():
    rpn = [2, -2, '+']
    assert rpn_binary(rpn) == [0]

    rpn = [3, 7, '*']
    assert rpn_binary(rpn) == [21]

    rpn = [8, 2, "recip", '/']
    assert rpn_binary(rpn) == [16]

    rpn = [-1, 3, '-', 2, '+', 4, "neg", 2, '**']
    assert rpn_binary(rpn) == [-2, 16]

    rpn = [3, -1, 9, '*', 22, 100, "neg", "sum"]
    assert rpn_binary(rpn) == [-84]


if __name__ == "__main__":
    test_unary()
    test_binary()
