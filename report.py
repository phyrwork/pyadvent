import click
import io
import itertools
import functools


from typing import Iterable
from operator import mul


@click.command()
@click.argument('report', type=click.File('rb'))
@click.argument('size', type=int)
def main(report: io.TextIOBase, size: int):
    values = map(lambda v: int(v), report)
    pairs = itertools.combinations(values, size)

    def match(p: Iterable[int]) -> bool:
        return sum(p) == 2020
    for t in filter(match, pairs):
        print(functools.reduce(mul, t))


if __name__ == '__main__':
    main()
