import click
import io

from typing import Iterator, List, Set, Dict


class Person(set, Set[str]):
    @property
    def qcount(self) -> Dict[str, int]:
        return {q: 1 for q in self}


class Group(list, List[Person]):
    @property
    def quniq(self) -> Set[str]:
        qs = set()
        for per in self:
            for q in per:
                qs.add(q)
        return qs

    @property
    def qcount(self) -> Dict[str, int]:
        qcs = {}
        for per in self:
            for q, n in per.qcount.items():
                qcs[q] = qcs.get(q, 0) + 1
        return qcs


def parse(txt: io.TextIOBase) -> Iterator[Group]:
    grp = Group()
    for line in txt:
        line: str = line.strip()
        if line == '':
            if grp:
                yield grp
                grp = Group()
            continue
        grp.append(Person(c for c in line))  # Person
    if grp:
        yield grp


@click.command()
@click.argument('manifest', type=click.File('r'))
def main(manifest: io.TextIOBase):
    grps = parse(manifest)
    count = 0
    for grp in grps:
        for _, n in grp.qcount.items():
            if n == len(grp):
                count += 1
    print(count)


if __name__ == '__main__':
    main()
