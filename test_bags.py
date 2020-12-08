# light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.

import pytest
import networkx

from typing import Dict

from .bags import parse, count_descends


@pytest.mark.parametrize(['rule', 'parent', 'children'], [
    pytest.param(
        'light red bags contain 1 bright white bag, 2 muted yellow bags.',
        'light red',
        {'bright white': 1, 'muted yellow': 2},
    ),
    pytest.param(
        'bright white bags contain 1 shiny gold bag.',
        'bright white',
        {'shiny gold': 1},
    ),
    pytest.param(
        'vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.',
        'vibrant plum',
        {'faded blue': 5, 'dotted black': 6},
    ),
])
def test_parse(rule: str, parent: str, children: Dict[str, int]):
    _parent, _children = parse(rule)
    assert _parent == parent
    assert _children == children


def test_count_descends():
    graph = networkx.DiGraph()
    graph.add_node('faded blue')
    graph.add_node('dotted black')
    graph.add_edge('faded blue', 'vibrant plum', count=5)
    graph.add_edge('dotted black', 'vibrant plum', count=6)
    graph.add_edge('faded blue',  'dark olive', count=3)
    graph.add_edge('dotted_black', 'dark olive', count=4)
    graph.add_edge('dark olive', 'shiny gold', count=1)
    graph.add_edge('vibrant plum', 'shiny gold', count=2)
    count = count_descends(graph, 'shiny gold')
    assert count == 32
