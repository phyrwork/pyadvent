import io

from .handheld import run


def test_first():
    prog = [
        ('nop', +0),
        ('acc', +1),
        ('jmp', +4),
        ('acc', +3),
        ('jmp', -3),
        ('acc', -99),
        ('acc', +1),
        ('jmp', -4),
        ('acc', +6),
    ]
    assert run(prog) == (False, 5)
