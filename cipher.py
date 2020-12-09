import itertools
import click
import io

from typing import Optional


@click.command()
@click.argument('records', type=click.File('r'))
def main(records: io.TextIOBase):
    # Ingest stream
    stream = []
    first: Optional[int] = None
    for record in records:
        value = int(record.strip())
        if (
            first is None
            and len(stream) > 25
            # Find first value not sum of pair in tail.
            and value not in map(
                lambda t: sum(t),
                itertools.combinations(stream[-25:], 2),
            )
        ):
            first = value
            print(first)
        stream.append(value)
    # Look for first contiguous set of numbers which sum to
    # first from above.
    for i in range(0, len(stream)):
        for j in range(i+2, len(stream)):  # At least len=2
            seg = stream[i:j]
            if sum(seg) == first:
                print(min(seg) + max(seg))
                exit(0)
    exit(1)


if __name__ == '__main__':
    main()
