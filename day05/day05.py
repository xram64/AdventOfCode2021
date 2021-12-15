## Advent of Code 2021: Day 5
## https://adventofcode.com/2021/day/5
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 5690, [Part 2]: 17741

import re
from PIL import Image
import numpy as np
from collections import namedtuple

# Lines will have the 'x' and 'y' values of the initial point of a line segment,
#   followed by the 'x' and 'y' values of the terminal point of the line segment.
Line = namedtuple('Line', ['i_x', 'i_y', 't_x', 't_y'])

# Closure for a line segment 'y = mx + b' function
def line_segment(m, b):
    def y(x):
        return (m*x + b)
    return y


if __name__ == '__main__':
    with open('day05_input.txt', 'r') as f:
        lines = f.readlines()

    # We'll assume the grid starts from (0, 0) (= top-left corner) and just define the height and width
    #   GRID_H: Value of the lowest vertical coord
    #   GRID_W: Value of the right-most horizontal coord
    GRID_H = 0
    GRID_W = 0

    all_coords = []

    for line in lines:
        grp = re.search(r'^(\d+),(\d+) -> (\d+),(\d+)$', line).groups()
        coord_map = Line( int(grp[0]), int(grp[1]), int(grp[2]), int(grp[3]) )

        all_coords.append(coord_map)

        # While we're here, update the grid boundaries with the given coords
        if max(coord_map.i_x, coord_map.t_x) > GRID_W:
            GRID_W = max(coord_map.i_x, coord_map.t_x)
        if max(coord_map.i_y, coord_map.t_y) > GRID_H:
            GRID_H = max(coord_map.i_y, coord_map.t_y)

    # Grid format:
    #   N = N vents overlap the grid point (default=0 for no vents)
    #   Array indices will correspond directly to the (1-indexed) coords, so we pad the array size by 1
    grid_hv = np.zeros((GRID_W+1, GRID_H+1))   # grid containing only horizontal and vertical lines
    grid = np.zeros((GRID_W+1, GRID_H+1))      # grid containing all lines


    # Iterate through all coords and update grid points with the number of vents that occupy them
    for coords in all_coords:
        # If x-coords are the same for each point, we have a vertical line
        if (coords.i_x == coords.t_x):
            # Iterate through all y-values and increment vent count for those grid coords
            left_y, right_y = min(coords.i_y, coords.t_y), max(coords.i_y, coords.t_y)
            for y in range(left_y, right_y+1):
                grid[coords.i_x, y] += 1
                grid_hv[coords.i_x, y] += 1  # also update "h-v" grid since this is a vertical line

        else:
            # For a non-vertical line, we'll need to find the slope and intercept of the line segment
            m = (coords.t_y - coords.i_y)/(coords.t_x - coords.i_x)
            b = coords.i_y - m*coords.i_x

            y = line_segment(m, b)

            # Iterate through all x-values between the initial and terminal x-coords and
            #   check if they have an integer y-value, based on the slope of the line
            # If so, increment the vent count for those grid coords
            left_x, right_x = min(coords.i_x, coords.t_x), max(coords.i_x, coords.t_x)

            for x in range(left_x, right_x+1):
                if y(x).is_integer():
                    grid[x, int(y(x))] += 1

                    # Only update "h-v" grid if this is a horizontal line
                    if (m == 0): grid_hv[x, int(y(x))] += 1


    # Output -- Console
    # for i in range(GRID_H):
    #     s = ""
    #     for j in range(GRID_W):
    #         if grid[i, j] == 0:
    #             s += "."
    #         else:
    #             s += str(int(grid[i, j]))
    #     print(s)


    ## Output -- Image
    # Make an image with 8-bit grayscale colors plus alpha channel
    img_part1 = Image.new('L', (GRID_W, GRID_H), 255)
    img_part2 = Image.new('L', (GRID_W, GRID_H), 255)

    # Map each value in the grid to a color value, darker for higher values
    # https://www.desmos.com/calculator/af3ywlndbh
    def color_map(n):
        return int(2**(-n+8) - 1)

    for i in range(GRID_H):
        for j in range(GRID_W):
            img_part1.putpixel( (i, j), color_map(int(grid_hv[i,j])) )
            img_part2.putpixel( (i, j), color_map(int(grid[i,j])) )

    img_part1.save('day05_part1.png')
    img_part2.save('day05_part2.png')


    ## Output -- Answer
    total_overlaps_hv = 0
    for value in np.nditer(grid_hv):
        if value >= 2: total_overlaps_hv += 1

    total_overlaps = 0
    for value in np.nditer(grid):
        if value >= 2: total_overlaps += 1

    print(f"[Part 1] There are {total_overlaps_hv} points where two or more horizontal or vertical lines overlap.")

    print(f"[Part 2] There are {total_overlaps} points where two or more lines of any kind overlap.")
