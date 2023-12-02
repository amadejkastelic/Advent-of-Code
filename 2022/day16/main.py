import collections
import itertools
import heapq

def parse_valves(s):
    valves = {}

    for line in s.splitlines():
        parts = line.split()
        valve = parts[1]
        flow_rate = int(parts[4][5:-1])
        lead_to = ''.join(parts[9:]).split(',')
        valves[valve] = (flow_rate, lead_to)

    valve_to_num = {}
    for key in sorted(valves.keys()):
        valve_to_num[key] = 1 << len(valve_to_num)

    valves = {
        valve_to_num[valve]: (flow_rate, tuple(map(valve_to_num.get, lead_to)))
        for valve, (flow_rate, lead_to) in valves.items()
    }

    return valves, valve_to_num

def part1(s):
    valves, valve_to_num = parse_valves(s)

    TOTAL_TIME = 30

    states = [(valve_to_num['AA'], 0, 0)]

    best = {}

    for t in range(1, TOTAL_TIME+1):
        print(t, len(states))

        new_states = []
        for loc, opened, pressure in states:
            key = (loc, opened)
            if key in best and pressure <= best[key]:
                continue

            best[key] = pressure

            flow_rate, lead_to = valves[loc]
            if loc & opened == 0 and flow_rate > 0:
                new_states.append((loc, opened | loc, pressure + flow_rate * (TOTAL_TIME - t)))
            for dest in lead_to:
                new_states.append((dest, opened, pressure))

        states = new_states

    answer = max(pressure for _, _, pressure in states)

    print(answer)

class _LazyDict(collections.defaultdict):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def __missing__(self, key):
        val = self.fn(key)
        self[key] = val
        return val

def make_lazy_dict(fn):
    return _LazyDict(fn)

def make_graph(neighbor_fn):
    def fn(key):
        return list(neighbor_fn(key))
    return make_lazy_dict(fn)

def dijkstra_length_fuzzy_end(graph, start, end_fn, heuristic=None):
    '''Returns the length of the shortest path from start to any end state
    in the graph. Return -1 if no path is found.
    graph[node] must return a list of (neighbor, distance) pairs
    Arguments:
    start - Either the starting state or a list of starting states
    end_fn - Function accepting a state. Returns True if this is an end state
    and False otherwise
    heuristic - If supplied, provides an estimate of the remaining distance
    from a given node to the end
    '''
    if heuristic is None:
        heuristic = lambda n: 0

    if not isinstance(start, list):
        start = [start]

    seen = set()
    queue = [(heuristic(s), 0, s) for s in start]
    heapq.heapify(queue)
    while len(queue) > 0:
        _, current_dist, current_node = heapq.heappop(queue)

        if end_fn(current_node):
            return current_dist

        if current_node in seen:
            continue
        seen.add(current_node)

        for neighbor_node, neighbor_dist in graph[current_node]:
            if neighbor_node in seen:
                continue
            new_dist = current_dist + neighbor_dist
            heapq.heappush(queue, (heuristic(neighbor_node) + new_dist,
                                   new_dist,
                                   neighbor_node))

    return -1

# This is abysmally slow. But it works.
# BFS was bogging down my memory, so I inverted this to a graph search for
# the least amount of *wasted* pressure. (AKA, pressure that could have been
# released had all the valves been open from the start.)
def part2(s):
    valves, valve_to_num = parse_valves(s)

    ALL_VALVES = 0
    for valve in valves.keys():
        assert(ALL_VALVES & valve == 0)
        ALL_VALVES = ALL_VALVES | valve

    TOTAL_TIME = 26

    MAXIMUM_FLOW_PER_TICK = 0
    for flow_rate, _ in valves.values():
        MAXIMUM_FLOW_PER_TICK += flow_rate

    TOTAL_MAXIMUM_FLOW = MAXIMUM_FLOW_PER_TICK * TOTAL_TIME

    def calc_sub_states(loc, opened):
        flow_rate, lead_to = valves[loc]
        if loc & opened == 0 and flow_rate > 0:
            yield loc, loc, flow_rate
        for dest in lead_to:
            yield dest, None, 0

    best_seen_time = TOTAL_TIME+1

    def neighbor_fn(state):
        self, elephant, opened, current_flow, time_remaining = state
        assert(time_remaining > 0)

        nonlocal best_seen_time
        if best_seen_time > time_remaining:
            print(time_remaining)
            best_seen_time = time_remaining

        if opened == ALL_VALVES:
            yield (None, None, opened, current_flow, time_remaining-1), 0
            return

        self_moves = list(calc_sub_states(self, opened))
        elephant_moves = list(calc_sub_states(elephant, opened))

        for ((dest1, open1, new_flow_1),
             (dest2, open2, new_flow_2)) in itertools.product(self_moves,
                                                              elephant_moves):
            if open1 is not None and open2 is not None and open1 == open2:
                continue
            new_opened = opened
            if open1 is not None:
                new_opened |= open1
            if open2 is not None:
                new_opened |= open2

            new_flow = current_flow + new_flow_1 + new_flow_2
            yield (dest1, dest2, new_opened, new_flow, time_remaining-1), MAXIMUM_FLOW_PER_TICK - current_flow

    graph = make_graph(neighbor_fn)

    start = (valve_to_num['AA'], valve_to_num['AA'], 0, 0, TOTAL_TIME)

    def end_fn(state):
        return state[-1] == 0

    least_missed_flow = dijkstra_length_fuzzy_end(graph, start, end_fn)

    answer = TOTAL_MAXIMUM_FLOW - least_missed_flow

    print(answer)

INPUT = open('2022/day16/input.txt').read()
part1(INPUT)
part2(INPUT)