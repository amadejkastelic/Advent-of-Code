import networkx as nx


def path(graph, source, target):
    try:
        return nx.shortest_path_length(graph, source, target)
    except:
        return -1


t = {
    complex(r, c): ord(s)
    for r, line in enumerate(open('2022/day12/input.txt'))
    for c, s in enumerate(line.strip())
}
s = next(k for k, v in t.items() if v == ord("S"))
e = next(k for k, v in t.items() if v == ord("E"))

t[s] = ord("a")
t[e] = ord("z")

G = nx.DiGraph()

for k, v in t.items():
    for d in (-1, 1, -1j, 1j):
        if (n := k + d) in t:
            if t[n] - v <= 1:
                G.add_edge(k, n)

print(nx.shortest_path_length(G, s, e))
print(min(l for k, v in t.items() if v == ord("a") and (l := path(G, k, e)) >= 0))
