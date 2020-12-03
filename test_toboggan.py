from .toboggan import Map


def test_map_contains():
    map_ = Map()
    map_.add((0, 0))
    map_.add((2, 1)) # width = 3
    assert (0, 0) in map_
    assert (3, 0) in map_
    assert (5, 1) in map_
    assert (2, 2) not in map_
