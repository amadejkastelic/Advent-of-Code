import dataclasses
import typing

import networkx
from matplotlib import pyplot

import solver


OP_MAP = {
    'AND': '&',
    'OR': '|',
    'XOR': '^',
}


@dataclasses.dataclass
class Expression:
    a: int
    b: int
    op: str

    def eval(self, wires: typing.Dict[str, int]) -> int:
        return eval(f'{wires[self.a]} {self.op} {wires[self.b]}')


class Solver(solver.Solver):
    def _init(self):
        self.graph = networkx.DiGraph()
        with open(self.input_file_path) as f:
            wires, expressions = f.read().split('\n\n')
        self.wires: typing.Dict[str, int] = {}
        for wire in wires.splitlines():
            name, val = wire.strip().split(': ')
            self.wires[name] = int(val)
        self.expressions: typing.Dict[str, Expression] = {}
        for expression in expressions.splitlines():
            gate, wire = expression.strip().split(' -> ')
            a, op, b = gate.strip().split()
            self.expressions[wire] = Expression(a, b, OP_MAP[op])
            self.graph.add_edge(a, wire, operator=op, color='red' if op == 'AND' else 'black')
            self.graph.add_edge(b, wire, operator=op, color='red' if op == 'AND' else 'black')

    def eval(self, wire: str) -> int:
        try:
            val = self.expressions[wire].eval(self.wires)
            self.wires[wire] = val
            return val
        except Exception:
            print(f'{wire} - {self.expressions[wire]}')
            pass

        self.eval(self.expressions[wire].a)
        self.eval(self.expressions[wire].b)
        val = self.expressions[wire].eval(self.wires)
        self.wires[wire] = val
        return val

    def _solve_part1(self) -> int:
        val = ''
        for wire in sorted(list(filter(lambda e: e.startswith('z'), self.expressions.keys())), reverse=True):
            val += str(self.eval(wire))
        return int(val, 2)

    def _solve_part2(self) -> str:
        colors = networkx.get_edge_attributes(self.graph, 'color').values()
        networkx.draw_networkx(self.graph, with_labels=True, edge_color=colors)
        pyplot.show()
        return 'https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder'
