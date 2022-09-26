# The game of life is a 2D cellular automaton: cells form a 2D grid,
# where each cell is either alive or dead. In each generation (step
# of the simulation), the new value of a given cell is computed from
# its value and the values of its 8 neighbours in the previous
# generation. The rules are as follows:
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
# Write a function which, given a set of live cells, computes the
# set of live cells after ‹n› generations. Live cells are given
# using their coordinates in the grid, i.e. as ‹(x, y)› pairs.

def life( cells, n ):
    pass


def test_main():
    assert life( set(), 3 ) == set()
    assert life( { ( 0, 0 ) }, 1 ) == set()
    block = { ( 0, 0 ), ( 1, 1 ), ( 0, 1 ), ( 1, 0 ) }

    blinker_0 = { ( 0, -1 ), ( 0, 0 ), ( 0, 1 ) }
    blinker_1 = { ( -1, 0 ), ( 0, 0 ), ( 1, 0 ) }
    glider    = blinker_1 | { ( 1, -1 ), ( 0, -2 ) }

    for i in range( 20 ):
        assert life( block, i ) == block, life( block, i )

    for i in range( 20 ):
        expect = blinker_0 if i % 2 == 0 else blinker_1
        assert life( blinker_0, i ) == expect

    for i in range( 0, 40, 4 ):
        expect = { ( x + i // 4, y + i // 4 ) for x, y in glider }
        assert life( glider, i ) == expect, \
               ( i, life( glider, i ), expect )

if __name__ == "__main__":
    test_main()
