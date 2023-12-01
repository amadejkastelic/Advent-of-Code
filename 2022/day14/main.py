import sys


lines = [line for line in open('2022/day14/input.txt').read().splitlines()]
paths = [ [list(map(int, s.split(","))) for s in line.split(" ->")] for line in lines ]

max_y = 0
blocks = set()
for path in paths:
  s_x, s_y = path[0]
  for p_x, p_y in path[1:]:
    if p_x == s_x:
      for y in range(min(s_y, p_y), max(s_y, p_y)+1):
        blocks.add((p_x, y))
        max_y = max(max_y, y)
    else:
      for x in range(min(s_x, p_x), max(s_x, p_x)+1):
        blocks.add((x, p_y))
      max_y = max(max_y, p_y)
    s_x, s_y = p_x, p_y

blocks0 = blocks.copy()
max_y += 2

src_x, src_y = (500, 0)

num_units = 0
abyss = False
while not abyss:
  p_x, p_y = src_x, src_y
  while True:
    down_blocks = any(b_x == p_x and b_y >= p_y for b_x, b_y in blocks)
    if not down_blocks:
      abyss = True
      break
    if (p_x, p_y+1) not in blocks:
      p_y += 1; continue
    if (p_x-1, p_y+1) not in blocks:
      p_x -= 1; p_y += 1; continue
    if (p_x+1, p_y+1) not in blocks:
      p_x += 1; p_y += 1; continue
    blocks.add((p_x, p_y))
    num_units += 1
    break

print(num_units)


blocks = blocks0

num_units = 0
blocked = False
while not blocked:
  p_x, p_y = src_x, src_y
  while True:
    if p_y+1 < max_y:
      if (p_x, p_y+1) not in blocks:
        p_y += 1; continue
      if (p_x-1, p_y+1) not in blocks:
        p_x -= 1; p_y += 1; continue
      if (p_x+1, p_y+1) not in blocks:
        p_x += 1; p_y += 1; continue
    if p_y == src_y:
      blocked = True
      break
    blocks.add((p_x, p_y))
    num_units += 1
    break

print(num_units+1)
