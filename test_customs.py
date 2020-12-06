import io

from .customs import parse


def test_parse():
    want = [
        [
            {'a', 'b', 'c'}
        ],
        [
            {'a'},
            {'b'},
            {'c'},
        ],
        [
            {'a', 'b'},
            {'a', 'c'},
        ],
        [
            {'a'},
            {'a'},
            {'a'},
            {'a'},
        ],
        [
            {'b'},
        ],
    ]
    got = list(parse(io.StringIO("""
        abc
        
        a
        b
        c
        
        ab
        ac
        
        a
        a
        a
        a
        
        b
    """)))
    assert got == want
