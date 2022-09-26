# Your task will be to implement a simple solver for ‘same game’.
# The rules of the game are:
#
#  1. the game is played on a rectangular board with ⟦n × m⟧
#     rectangular cells,
#  2. a cell can be empty, or occupied by a ‘stone’ of a particular
#     type (we will use numbers to represent these types, and ‹None›
#     to represent an empty cell),
#  3. the player can remove an area made up of 3 or more identical
#     adjacent stones (each stone has 4 neighbours); all matching
#     stones are removed at once,
#  4. the game ends when no more stones can be removed.
#
# Unlike most versions of the game, to keep things simple, we will
# not implement gravity or replenishment of the stones (at least not
# in this iteration). The scoring rules are as follows:
#
#  1. the base score of removal is the value of the stone ⟦v⟧ times the
#     number of stones ⟦n⟧ removed from the board times the base-2
#     logarithm of the same: ⟦v⋅n⋅\log₂(n)⟧, the entire number
#     rounded to the closest integer,
#  2. this score is doubled if the removal is in an area directly
#     adjacent to stones removed in the last round,
#  3. it is also doubled if the last removal was of the same type of
#     stone (note that conditions 2 and 3 are mutually exclusive).
#
# When the game ends, the scores for each round are summed: this is
# the game score.
#
# Write a function ‹samegame› which takes 2 arguments: the initial
# board in the form of a single list of numbers (with ‹None› used to
# represent empty spaces) and the width of the playing board. You
# can assume that the number of items in the list will be an integer
# multiple of the width. The result of the function should be the
# maximum achievable game score.

def samegame( board: list[ int ], width: int ) -> int:
    pass
