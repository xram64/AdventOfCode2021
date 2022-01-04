## Advent of Code 2021: Day 9
## https://adventofcode.com/2021/day/9
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 444, [Part 2]:

import numpy as np
from collections import namedtuple
from PIL import Image

# [Part 1: Scan over all locations, recording any local minima found within each location's L₁-norm neighborhood (with radius 1).]

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


def constructGradient(stops):
    # Expects a list of four RGB colors with format '#ffffff'
    if len(stops) != 4: raise ValueError('Expects 4 color stops.')

    # Parse colors into components
    stopComps = []
    for stop in stops:
        stopComps.append( (int(stop[1:3], 16), int(stop[3:5], 16), int(stop[5:7], 16)) )

    gradient = [0]*10

    gradient[0] = stopComps[0]
    gradient[3] = stopComps[1]
    gradient[6] = stopComps[2]
    gradient[9] = stopComps[3]

    for i in [0, 1, 2]:
        step_r = int( abs(stopComps[i+1][0] - stopComps[i][0]) / 3 )  # r
        step_g = int( abs(stopComps[i+1][1] - stopComps[i][1]) / 3 )  # g
        step_b = int( abs(stopComps[i+1][2] - stopComps[i][2]) / 3 )  # b
        gradient[3*i+1] = tuple(map( lambda x,y: x+y, stopComps[i], (step_r, step_g, step_b) ))
        gradient[3*i+2] = tuple(map( lambda x,y: x+y, stopComps[i], (2*step_r, 2*step_g, 2*step_b) ))

    return gradient


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

    # Create image of heightmap
    img_heightmap = Image.new('RGB', (heightmap_dims.cols, heightmap_dims.rows))
    img_heightmap_scale = 4

    gradient = constructGradient(['#555555', '#8e6810', '#ac590b', '#a43111'])
    colormap = {}
    for n, color in enumerate(gradient):
        colormap[n] = color

    for j in range(heightmap_dims.rows):
        for i in range(heightmap_dims.cols):
            img_heightmap.putpixel( (i, j), colormap[heightmap[i,j]])

    img_heightmap = img_heightmap.resize((img_heightmap_scale*heightmap_dims.cols, img_heightmap_scale*heightmap_dims.rows), resample=Image.NEAREST)
    img_heightmap.save('day09_heightmap.png')


    ## Part 2
