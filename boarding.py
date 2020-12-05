import click
import io

from typing import Tuple
from itertools import product

# Binary space partitioning means
# we can just convert the code into
# binary numbers.

F = 0
B = 1

L = 0
R = 1


Seat = Tuple[int, int]  # row, col
ROW = 0
COL = 1


def parse(code: str) -> Seat:
    row = int(''.join([
        '0' if c == 'F' else '1'
        for c
        in code[:7]
    ]), 2)
    col = int(''.join([
        '0' if c == 'L' else '1'
        for c
        in code[7:]
    ]), 2)
    return row, col


@click.command()
@click.argument('codes', type=click.File('r'))
def main(codes: io.TextIOBase):
    ids_ = set()
    for code in codes:
        code: str = code.strip()
        seat = parse(code)
        id_ = (seat[ROW] * 8) + seat[COL]
        ids_.add(id_)
    ordered = sorted(ids_)
    for i in range(0, len(ordered)):
        cur, next_ = ordered[i], ordered[i+1]
        if next_ != cur + 1:
            print(cur + 1)
            return


if __name__ == '__main__':
    main()
