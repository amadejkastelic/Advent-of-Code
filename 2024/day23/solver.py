import networkx

import solver


class Solver(solver.Solver):
    def _init(self):
        self.graph = networkx.Graph()
        with open(self.input_file_path) as f:
            for line in f.readlines():
                self.graph.add_edge(*line.strip().split('-'))

    def _solve_part1(self) -> int:
        res = 0
        for clique in networkx.enumerate_all_cliques(self.graph):
            if len(clique) != 3:
                continue
            for node in clique:
                if node.startswith('t'):
                    res += 1
                    break
        return res

    def _solve_part2(self) -> int:
        return ','.join(sorted(max(networkx.find_cliques(self.graph), key=len)))
