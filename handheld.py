import click
import io
import copy

from typing import List, Tuple


@click.command()
@click.argument('src', type=click.File('r'))
def main(src: io.TextIOBase):
    # Read program
    prog = []
    for line in src:
        line: str = line.strip()
        if line == '':
            continue
        args = line.split(' ')
        inst = (args[0], int(args[1]))
        prog.append(inst)
    print(run(prog))

    # Find jmp/nop
    inds = [
        i
        for i, inst
        in enumerate(prog)
        if inst[0] in {'jmp', 'nop'}
    ]
    # Flip instructions, find first to fix program
    for ind in inds:
        mprog = copy.copy(prog)
        mprog[ind] = (
            'jmp' if mprog[ind][0] == 'nop' else 'nop',
            mprog[ind][1],
        )
        term, acc = run(mprog)
        if term:
            print(term, acc)
            exit(0)
    exit(1)


def run(prog: List[Tuple[str, int]]) -> (bool, int):
    pc = 0
    acc = 0

    # Instructions
    def facc(arg: int):
        nonlocal acc
        acc += arg

    def fjmp(arg: int):
        nonlocal pc
        pc += (arg - 1)

    def fnop(_: int):
        pass

    isa = {
        'acc': facc,
        'jmp': fjmp,
        'nop': fnop,
    }

    execs = {}
    while True:
        if execs.get(pc, 0) == 1:  # before exec #2
            return False, acc
        execs[pc] = execs.get(pc, 0) + 1
        inst = prog[pc]
        isa[inst[0]](inst[1])
        pc += 1
        if pc > len(prog):
            # OOB
            return False, 0
        if pc == len(prog):
            # Terminates corect by executing first
            # instruction after program.
            return True, acc


if __name__ == '__main__':
    main()
