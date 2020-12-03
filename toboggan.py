import click
import io
import typing


Coord = typing.Tuple[int, int]
X = 0
Y = 1


class Map(set, typing.Set[Coord]):
    def __init__(self):
        super(Map, self).__init__()
        self.at: typing.Set[Coord] = set()
        self.xmax: typing.Optional[int] = None
        self.ymax: typing.Optional[int] = None

    @property
    def w(self) -> int:
        if self.xmax is None:
            return 0
        return self.xmax + 1

    @property
    def h(self) -> int:
        if self.ymax is None:
            return 0
        return self.ymax + 1

    def add(self, co: Coord):
        super(Map, self).add(co)
        if self.xmax is None or co[X] > self.xmax:
            self.xmax = co[X]
        if self.ymax is None or co[Y] > self.ymax:
            self.ymax = co[Y]

    def __contains__(self, co: Coord) -> bool:
        if self.xmax is None:
            return False
        _co = (co[X] % self.w, co[Y])
        return super(Map, self).__contains__(_co)

    @classmethod
    def read(cls, in_: io.TextIOBase):
        out = Map()
        for y, line in enumerate(in_):
            line: str = line.strip()
            for x, b in enumerate(line):
                s = chr(b)
                if s == '#':
                    out.add((x, y))
        return out


def parse_gradient(gradstr: str) -> Coord:
    strco = gradstr.split(',')
    return int(strco[X]), int(strco[Y])


@click.command()
@click.argument('in_', type=click.File('rb'))
@click.argument('gradients', nargs=-1, type=str)
def main(in_: io.TextIOBase, gradients: typing.List[str]):
    map_ = Map.read(in_)
    prod = 1
    for gradstr in gradients:
        gradient = parse_gradient(gradstr)
        cur = (0, 0)
        count = 0
        while cur[Y] <= map_.ymax:
            if cur in map_:
                count += 1
            cur = (cur[X] + gradient[X], cur[Y] + gradient[Y])
        prod *= count
    print(prod)


if __name__ == '__main__':
    main()
