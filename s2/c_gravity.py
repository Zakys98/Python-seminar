# In this task, we will continue with the implementation of ‘same
# game’ from the first set. All the rules remain the same (ha-ha)
# except that gravity causes the board to reshuffle when more than
# ⟦nm/10⟧ stones are removed all at once (where the board has
# ⟦n x m⟧ cells). A stone will fall if it is are either:
#
#  • «unsupported» - there is an empty cell right below it, or
#  • «unstable» – a stone is unstable on the left if it is missing
#    both its direct left neighbour and the bottom-left diagonal
#    neighbour (instability on the right is symmetrical); however
#    edges of the board are considered stable (they do «not» count
#    as ‘missing a neighbour’).
#
# At most one stone is falling at any given time. The first stone to
# fall is the one nearest to the bottom (if there are multiple such
# stones, the leftmost one falls first).
#
# The mechanics of the fall are as follows:
#
#  1. an unsupported stone will fall in a straight line toward the
#     bottom until it hits another stone,
#  2. an unstable stone will roll off its position, by moving either
#     to the empty cell below and to its left (or right, if it
#     cannot roll to the left),
#  3. a stone that started to fall will continue to fall until it is
#     both supported and stable (on both sides),
#  4. if a stone becomes unsupported due to another stone falling,
#     it will be the next to fall (this does not apply to stones
#     that become unstable – those are processed in the usual
#     bottom-up, left-to-right order).
#
# The reshuffle is considered part of the round that caused it. The
# scoring rule about adjacent removals remains otherwise unchanged
# (i.e. it might be triggered by a cell whose stone went missing due
# to gravity, and vice-versa, the bonus is not awarded when removing
# stones that got buried by an earthquake).
#
# The entry point, ‹samegame›, is also unchanged.
