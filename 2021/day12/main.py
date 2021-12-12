import typing


def main():
    file_name = input('Enter input path: ')

    with open(file_name, 'r') as f:
        content = f.readlines()

    graph: typing.Dict[str, typing.Set[str]] = {}
    for line in content:
        a, b = line.strip().split('-')
        graph[a] = graph.get(a, set()).union({b})
        graph[b] = graph.get(b, set()).union({a})

    paths = []
    _find_all_paths_dfs(graph=graph, visited=set(), path=[], paths=paths)
    print(f'Part 1: {len(paths)}')

    paths = []
    _find_all_paths_dfs_v2(graph=graph, visited={}, path=[], paths=paths)
    print(f'Part 2: {len(paths)}')


def _find_all_paths_dfs(
    graph: typing.Dict[str, typing.Set[str]],
    visited: typing.Set[str],
    path: typing.List[str],
    paths: typing.List[typing.List[str]],
    current: str = 'start',
    end: str = 'end',
):
    if not current.isupper():
        visited.add(current)
    path.append(current)

    if current == end:
        paths.append(path)
    else:
        for neighbor in graph[current]:
            if neighbor not in visited:
                _find_all_paths_dfs(
                    graph=graph, visited=visited, path=path, current=neighbor, end=end, paths=paths
                )

    path.pop()
    if not current.isupper():
        visited.remove(current)


def _find_all_paths_dfs_v2(
        graph: typing.Dict[str, typing.Set[str]],
        visited: typing.Dict[str, int],
        path: typing.List[str],
        paths: typing.List[typing.List[str]],
        current: str = 'start',
        end: str = 'end',
):
    if not current.isupper():
        visited[current] = visited.get(current, 0) + 1

    path.append(current)

    if current == end:
        paths.append(path)
    else:
        for neighbor in graph[current]:
            if visited.get(neighbor, 0) < 1 or (neighbor != 'start' and all(value != 2 for value in visited.values())):
                _find_all_paths_dfs_v2(
                    graph=graph, visited=visited, path=path, current=neighbor, end=end, paths=paths
                )

    path.pop()
    if not current.isupper():
        visited[current] = visited[current] - 1


if __name__ == '__main__':
    main()
