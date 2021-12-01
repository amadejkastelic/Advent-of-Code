def count_increases(depths, sliding_window=1):
    sliding_depths = []
    for i in range(len(depths)):
        sliding_depths.append(sum(depths[i:i+sliding_window]))

    count = 0
    for i in range(1, len(sliding_depths)):
        if sliding_depths[i] > sliding_depths[i-1]:
            count += 1
    return count


if __name__ == '__main__':
    file_name = input("Enter input path: ")

    with open(file_name, 'r') as f:
        content = f.read().splitlines()

    depths = [int(depth) for depth in content]

    print(count_increases(depths=depths))
    print(count_increases(depths=depths, sliding_window=3))
