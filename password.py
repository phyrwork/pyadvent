import click
import re
import io


from typing import Type


class Policy:
    def validate(self, pw: str) -> bool:
        raise NotImplementedError

    @classmethod
    def parse(cls, policy: str) -> 'Policy':
        raise NotImplementedError


class PositionPolicy(Policy):
    REGEXP = re.compile(r'(\d+)-(\d+)\s(\w)')

    def __init__(
        self,
        char: str,
        pos_a: int,
        pos_b: int,
    ):
        self.char: str = char
        self.pos_a: int = pos_a
        self.pos_b: int = pos_b

    @classmethod
    def parse(cls, policy: str) -> 'PositionPolicy':
        match = cls.REGEXP.search(policy)
        if match is None:
            raise ValueError('not a policy string: {0}'.format(policy))
        return cls(
            match.group(3),
            int(match.group(1)),
            int(match.group(2)),
        )

    def has_char_at(self, pw: str, pos: int) -> bool:
        if pos > len(pw):
            return False
        return pw[pos - 1] == self.char

    def validate(self, pw: str) -> bool:
        count = 0
        if self.has_char_at(pw, self.pos_a):
            count += 1
        if self.has_char_at(pw, self.pos_b):
            count += 1
        return count == 1


class CountPolicy(Policy):
    REGEXP = re.compile(r'(\d+)-(\d+)\s(\w)')

    def __init__(
        self,
        char: str,
        min_count: int,
        max_count: int,
    ):
        self.char: str = char
        self.min_count: int = min_count
        self.max_count: int = max_count

    @classmethod
    def parse(cls, policy: str) -> 'CountPolicy':
        match = cls.REGEXP.search(policy)
        if match is None:
            raise ValueError('not a policy string: {0}'.format(policy))
        return cls(
            match.group(3),
            int(match.group(1)),
            int(match.group(2)),
        )

    def validate(self, pw: str) -> bool:
        counts = {}
        for char in pw:
            counts[char] = counts.get(char, 0) + 1
        want = counts.get(self.char, 0)
        if want < self.min_count:
            return False
        if want > self.max_count:
            return False
        return True


POLICIES = {
    'count': CountPolicy,
    'position': PositionPolicy,
}


def get_policy(ctx, param, value) -> Type[Policy]:
    return POLICIES[value]


@click.command()
@click.argument('passwords', type=click.File('rb'))
@click.argument('policy_type')
def main(passwords: io.TextIOBase, policy_type: str):
    policy_cls = POLICIES[policy_type]
    ok = 0
    for _policy, pw in map(lambda line: str.split(str(line), ': '), passwords):
        pw: str = pw.rstrip('\n')
        policy = policy_cls.parse(_policy)
        if policy.validate(pw):
            ok += 1
    print(ok)


if __name__ == '__main__':
    main()
