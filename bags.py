import re
import click
import io
import networkx
import functools

from typing import Dict


def parse(rule: str) -> (str, Dict[str, int]):
    match = re.compile(
        r'^(((\w| )+) bags?) contain ((((\d+) ((\w| )+) bags?)(, ((\d+) ((\w| )+) bags?))*)|no other bags).$',
    ).match(rule)
    if match is None:
        raise ValueError('not a rule: {0}', rule)
    parent = match.group(2)
    subrules = match.group(5)
    if subrules is None:
        return parent, {}
    children: Dict[str, int] = {}
    for subrule in subrules.split(', '):
        match = re.compile(
            r'(\d+) ((\w| )+) bags?',
        ).match(subrule)
        if match is None:
            raise ValueError('not a rule part: {0}', subrule)
        children[match.group(2)] = int(match.group(1))
    return parent, children


def count_descends(graph: networkx.DiGraph, node: str) -> int:
    total = 0
    for child, _ in graph.in_edges(node):
        count = 1 + count_descends(graph, child)
        multiplier = graph.get_edge_data(child, node)['count']
        total += multiplier * count
    return total


@click.command()
@click.argument('rules', type=click.File('r'))
def main(rules: io.TextIOBase):
    # Make a graph of bag membership
    graph = networkx.DiGraph()
    for rule in rules:
        rule: str = rule.strip()
        parent, children = parse(rule)
        for child, count in children.items():
            graph.add_edge(child, parent, count=count)

    print(count_descends(graph, 'shiny gold'))


if __name__ == '__main__':
    main()
