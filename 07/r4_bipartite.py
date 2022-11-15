# An undirected graph is given as a set of edges ⟦E⟧. For any ⟦(u,
# v) ∈ E⟧, it must also be true that ⟦(v, u) ∈ E⟧. The set of
# vertices is implicit (i.e. it contains exactly the vertices which
# appear in ⟦E⟧).
#
# Below is a predicate which should decide whether a given graph is
# bipartite (can be coloured with at most 2 colours, such that no
# edge goes between vertices of the same colour). Make sure it is
# correct, or fix it.
import hypothesis.strategies as s
import hypothesis


@hypothesis.given(s.integers(min_value=3, max_value=100).filter(lambda n : n % 2 == 1))
def test(n):
    edge_set = set()
    for i in range(n):
        a, b = i, (i +1) % n
        edge_set.add((a,b))
        edge_set.add((b,a))

    assert is_bipartite(edge_set) == (n % 2 == 0)

def is_bipartite( graph ):
    colours = {}
    queue = []

    vertices = list( set( [ x for x,_ in graph ] ) )
    for v in vertices: # can be disconnected
        if v in colours:
            continue
        queue.append( v )
        colours[ v ] = 1
        colour = 1

        while queue:
            v = queue.pop( 0 )
            colour = 2 if colours[ v ] == 1 else 1
            for neighb in [ y for x, y in graph if x == v ]:
                if neighb in colours and \
                   colours[ neighb ] != colour:
                    return False
                if neighb not in colours:
                    colours[ neighb ] = colour
                    queue.append( neighb )
    return True

def zdar(func):
    return func(5)

@zdar
def lol(n):
    return n


if __name__=='__main__':
    test()
    print(lol)