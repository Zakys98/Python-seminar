# Given an undirected graph in the form of a set of 2-tuples (see
# below), decide whether the graph is bipartite. That is, whether
# each vertex can be assigned one of 2 colours, such that no edge
# goes between vertices of the same colour. Hint: BFS.
#
# The graph is given as a set of edges ⟦E⟧. For any ⟦(u, v) ∈ E⟧, it
# is also true that ⟦(v, u) ∈ E⟧ (you can assume this in your
# algorithm). The set of vertices is implicit (i.e. it contains
# exactly the vertices which appear in ⟦E⟧).

def is_bipartite(graph):
    pass

def test_main():
    g = { ( 1, 2 ), ( 2, 1 ) }
    h = { ( 1, 2 ), ( 1, 3 ), ( 2, 1 ), ( 3, 1 ) }
    i = { ( 1, 2 ), ( 1, 3 ), ( 2, 3 ),
          ( 2, 1 ), ( 3, 1 ), ( 3, 2 ) }
    j = { ( 1, 2 ), ( 1, 3 ), ( 1, 4 ),
          ( 2, 3 ), ( 2, 4 ), ( 3, 4 ),
          ( 2, 1 ), ( 3, 1 ), ( 4, 1 ),
          ( 3, 2 ), ( 4, 2 ), ( 4, 3 ) }
    k = { ( 1, 2 ), ( 2, 3 ), ( 3, 4 ), ( 4, 1 ),
          ( 2, 1 ), ( 3, 2 ), ( 4, 3 ), ( 1, 4 ) }
    l = { ( 1, 2 ), ( 3, 4 ), ( 4, 5 ), ( 3, 5 ),
          ( 2, 1 ), ( 4, 3 ), ( 5, 4 ), ( 5, 3 ) }

    assert is_bipartite( g )
    assert is_bipartite( h )
    assert not is_bipartite( i )
    assert not is_bipartite( j )
    assert is_bipartite( k )
    assert not is_bipartite( l )

if __name__ == "__main__":
    test_main()
