import click
import io
import re

from typing import Iterator, Dict


def parse(in_: io.TextIOBase) -> Iterator[Dict[str, str]]:
    cur = {}
    for line in in_:
        line: str = line.strip()
        if line == '':
            if cur:
                yield cur
            cur = {}
            continue
        for fld in line.split(' '):
            parts = fld.split(':')
            cur[parts[0]] = parts[1]
    if cur:
        yield cur


def validate_yr_between(lo: int, hi: int, s: str) -> bool:
    if re.compile(r'^\d{4}$').match(s) is None:
        return False
    return lo <= int(s) <= hi


def validate_hgt(s: str) -> bool:
    match = re.compile(r'^(\d+)(cm|in)$').match(s)
    if match is None:
        return False
    unit = match.group(2)
    count = int(match.group(1))
    if unit == 'cm':
        return 150 <= count <= 193
    if unit == 'in':
        return 59 <= count <= 76
    return False


def validate_hcl(s: str) -> bool:
    return re.compile(r'^#[0-9a-f]{6}$').match(s) is not None


def validate_ecl(s: str) -> bool:
    return s in {
        'amb',
        'blu',
        'brn',
        'gry',
        'grn',
        'hzl',
        'oth',
    }


def validate_pid(s: str) -> bool:
    return re.compile(r'^\d{9}$').match(s) is not None


FIELDS = {
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
}


def validate(passport: Dict[str, str]) -> bool:
    return (
        passport.keys() & FIELDS == FIELDS
        and validate_yr_between(1920, 2002, passport['byr'])
        and validate_yr_between(2010, 2020, passport['iyr'])
        and validate_yr_between(2020, 2030, passport['eyr'])
        and validate_hgt(passport['hgt'])
        and validate_hcl(passport['hcl'])
        and validate_ecl(passport['ecl'])
        and validate_pid(passport['pid'])
    )


@click.command()
@click.argument('manifest', type=click.File('r'))
def main(manifest: io.TextIOBase):
    count = 0
    for passport in parse(manifest):
        if validate(passport):
            count += 1
    print(count)


if __name__ == '__main__':
    main()
