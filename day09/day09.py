## Advent of Code 2021: Day 9
## https://adventofcode.com/2021/day/9
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 444, [Part 2]:

import numpy as np
from collections import namedtuple

# [Scan over all locations, recording any local minima found within each location's L₁-norm neighborhood (with radius 1).]

Dims = namedtuple('Dimensions', ['rows', 'cols'])
Pos = namedtuple('Position', ['y', 'x'])  # reversed axes to match row-col order
Adjacent = namedtuple('Adjacencies', ['up', 'right', 'down', 'left'])

def findRiskLevel(map, pos, dims):
    # If this point is a local minimum (low point), return its risk level (always >1).
    # Otherwise, return 0.

    # Get adjacent coords for this position, setting invalid coords (on map boundary) to None
    # Up
    if pos.y == 0: adj_up = None
    else: adj_up = Pos(x=pos.x, y=pos.y-1)

    # Right
    if pos.x == dims.cols-1: adj_right = None
    else: adj_right = Pos(x=pos.x+1, y=pos.y)

    # Down
    if pos.y == dims.rows-1: adj_down = None
    else: adj_down = Pos(x=pos.x, y=pos.y+1)

    # Left
    if pos.x == 0: adj_left = None
    else: adj_left = Pos(x=pos.x-1, y=pos.y)

    adjacencies = Adjacent(adj_up, adj_right, adj_down, adj_left)
    for adj in adjacencies:
        if adj:
            # If the height of the current pos is >= any valid adjacent position, this is not a low point.
            if map[pos] >= map[adj]:
                return 0
    else:
        # If all valid adjacent heights are higher, return (1 + height) as the risk level for this position.
        return (1 + map[pos])



if __name__ == '__main__':

    with open('day09_input.txt', 'r') as f:
        temparray = []
        for line in f.readlines():
            row = [int(num) for num in list(line.strip())]
            temparray.append(row)

    ## Part 1
    heightmap = np.array(temparray)
    heightmap_dims = Dims(*heightmap.shape)

    total_risk_level = 0
    low_point_count = 0

    for r in range(heightmap_dims.rows):
        for c in range(heightmap_dims.cols):
            pos = Pos(r, c)

            risk = findRiskLevel(heightmap, pos, heightmap_dims)
            total_risk_level += risk

            if (risk > 0): low_point_count += 1

    print(f"[Part 1] There are {low_point_count} low points in the heightmap with a total risk level of {total_risk_level}.")
