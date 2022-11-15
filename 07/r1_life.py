# Remember the game of life from week 1? A quick reminder: it is a
# 2D cellular automaton where each cell is either alive or dead. In
# each generation (step of the simulation), the new value of a given
# cell is computed from its value and the values of its 8 neighbours
# in the previous generation. The rules are as follows:
#
# │ state │ alive neigh. │ result │
# ├───────┼──────────────┼────────┤
# │ alive │          0–1 │   dead │
# │ alive │          2–3 │  alive │
# │ alive │          4–8 │   dead │
# │┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄│
# │  dead │          0–2 │   dead │
# │  dead │            3 │  alive │
# │  dead │          4-8 │   dead │
#
# An example of a short periodic game:
#
#  ┌───┬───┬───┐   ┌───┬───┬───┐   ┌───┬───┬───┐
#  │   │   │   │   │   │ ○ │   │   │   │   │   │
#  ├───┼───┼───┤   ├───┼───┼───┤   ├───┼───┼───┤
#  │ ○ │ ○ │ ○ │ → │   │ ○ │   │ → │ ○ │ ○ │ ○ │
#  ├───┼───┼───┤   ├───┼───┼───┤   ├───┼───┼───┤
#  │   │   │   │   │   │ ○ │   │   │   │   │   │
#  └───┴───┴───┘   └───┴───┴───┘   └───┴───┴───┘
#
# Enclosed is an implementation of the game that is maybe correct,
# but maybe not. Write tests and find out which it is. Fix the bugs
# if you find any.

import hypothesis
import hypothesis.strategies as s

def updated( x, y, cells ):
    count = 0
    alive = ( x, y ) in cells

    for dx in [ -1, 0, 1 ]:
        for dy in [ -1, 0, 1 ]:
            if dx and dy:
                count += ( x + dx, y + dy ) in cells

    return count in { 2, 3 } if alive else count == 3

def life( cells, n ):
    if n == 0:
        return cells

    todo = set()

    for x, y in cells:
        for dx in [ -1, 0, 1 ]:
            for dy in [ -1, 0, 1 ]:
                todo.add( ( x + dx, y + dy ) )

    ngen = { ( x, y ) for x, y in todo if updated( x, y, cells ) }
    return life( ngen , n - 1 )

@hypothesis.given(s.integers(), s.integers())
def test_life(life):
    pass
