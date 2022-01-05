## Advent of Code 2021: Day 9
## https://adventofcode.com/2021/day/9
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 444, [Part 2]: 1168440

import numpy as np
from collections import namedtuple, OrderedDict, deque
from PIL import Image, ImageColor

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


def constructGradient(stops, highlightEdges=None):
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
        def addColors(c1, c2, step):
            if (c1 < c2): return c1 + step    # going up
            elif (c2 < c1): return c1 - step  # going down
            else: return c1  # same value
        gradient[3*i+1] = tuple(map( addColors, stopComps[i], stopComps[i+1], (step_r, step_g, step_b) ))
        gradient[3*i+2] = tuple(map( addColors, stopComps[i], stopComps[i+1], (2*step_r, 2*step_g, 2*step_b) ))

    # Optional: Highlight edges (9's) in map with a different color
    if highlightEdges:
        gradient[9] = (int(highlightEdges[1:3], 16), int(highlightEdges[3:5], 16), int(highlightEdges[5:7], 16))

    return gradient


def _scanLeftRight(pos, map):
    # Find the nearest borders to the given position within its row
    left_border_idx, right_border_idx = -1, map.shape[1]  # set defaults to just outside of map in case basin is adjacent to an edge
    row_iter = np.nditer(map[pos.y, :], flags=['f_index'])

    for e in row_iter:
        if (row_iter.index < pos.x) and (e == 1):
            left_border_idx = row_iter.index  # save last encountered border, up to the given position
        elif (row_iter.index > pos.x) and (e == 1):
            right_border_idx = row_iter.index  # save next encountered border after the given position
            break

    # Return the list of potentially new basin positions found between the borders
    return [Pos(x=i, y=pos.y) for i in range(left_border_idx+1, right_border_idx)]

def _scanUpDown(pos, map):
    # Find the nearest borders to the given position within its row
    up_border_idx, down_border_idx = -1, map.shape[0]  # set defaults to just outside of map in case basin is adjacent to an edge
    col_iter = np.nditer(map[:, pos.x], flags=['f_index'])

    for e in col_iter:
        if (col_iter.index < pos.y) and (e == 1):
            up_border_idx = col_iter.index  # save last encountered border, up to the given position
        elif (col_iter.index > pos.y) and (e == 1):
            down_border_idx = col_iter.index  # save next encountered border after the given position
            break

    # Return the list of potentially new basin positions found between the borders
    return [Pos(x=pos.x, y=j) for j in range(up_border_idx+1, down_border_idx)]

def exploreBasin(lowpt, map, anim_basin=None):
    # Basin scanning algorithm:
    #  - Starting with a low point, scan left and right until a border (1) is hit.
    #  - From each point found in the left-right scan, scan up and down until a border is hit.
    #  - From each of these new points, scan left and right, and so on.
    #  - Once a full scan in either direction has completed without adding any new points, all points in the basin have been identified.

    max_depth = 25  # max iteration depth for the entire scan
    _nextScan = [_scanUpDown, _scanLeftRight]  # function list to alternate scan axes
    n = 0  # index to set next scan function

    basinPositions = set()

    # Get positions of all basin elements left and right from the initial low point
    scanList = _scanLeftRight(lowpt, map)
    lastPositions = set(scanList)
    basinPositions |= lastPositions

    # (Optional) Add new positions to animation list
    if anim_basin != None: anim_basin += scanList

    # Alternate scanning up-down and left-right until all basin positions have been discovered
    for _ in range(max_depth):
        # For each of the last-found positions, scan along the opposite axis for new positions
        newPositions = set()
        for pos in lastPositions:
            # Gather all scanned positions into the newPositions set
            scanList = _nextScan[n](pos, map)
            newPositions |= set(scanList)

            # (Optional) Add new positions to animation list
            if anim_basin != None: anim_basin += [p for p in scanList if p not in anim_basin]

        # If we've already seen all of these new positions, we can assume all basin positions have been found
        if set(newPositions) <= set(basinPositions):  # subset check
            break
        else:
            # If we did find new positions, collect only the ones not seen before into the lastPositions set
            lastPositions = newPositions - basinPositions
            # Then union these new positions into the basinPositions set
            basinPositions |= lastPositions

        # Set up next scan axis
        n = (n + 1)%2
    else:
        print(f'Max iteration depth of {max_depth} reached!')

    return list(basinPositions)


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
    low_points = []

    for r in range(heightmap_dims.rows):
        for c in range(heightmap_dims.cols):
            pos = Pos(r, c)

            risk = findRiskLevel(heightmap, pos, heightmap_dims)
            total_risk_level += risk

            # If we found a low point here (non-zero risk), add its position to the list of low points
            if (risk > 0):
                low_points.append(pos)

    print(f"[Part 1] There are {len(low_points)} low points in the heightmap with a total risk level of {total_risk_level}.")

    ## Part 1 - Image
    # Create image of heightmap
    img_heightmap = Image.new('RGBA', (heightmap_dims.cols, heightmap_dims.rows))
    img_heightmap_scale = 4

    gradient = constructGradient(['#484848', '#a68f2c', '#9a6619', '#90200c'], highlightEdges='#751707')
    colormap = {}
    for n, color in enumerate(gradient):
        colormap[n] = color

    for j in range(heightmap_dims.rows):
        for i in range(heightmap_dims.cols):
            img_heightmap.putpixel((i, j), colormap[heightmap[j,i]])

    img_heightmap_resized = img_heightmap.resize((img_heightmap_scale*heightmap_dims.cols, img_heightmap_scale*heightmap_dims.rows), resample=Image.NEAREST)
    img_heightmap_resized.save('day09_heightmap.png')


    ## Part 2
    # First, convert the heightmap into a binary "basin map" where the walls (9's) are mapped to 1 and all other positions are mapped to 0.
    basinmap = heightmap.copy()
    basinmap[basinmap <= 8] = 0
    basinmap[basinmap == 9] = 1

    # Set up a list to keep track of coords for the scanning animation
    # Each basin will have its own sub-list in scanning order made of the list of coords for each basin, added in the order they're found
    # Format:  [[Basin1], [Basin2], ...] = [[(2,2), (2,3), (3,2)], [(4,1), (4,2)], ...]
    anim_coords = []

    # Find the size of each basin
    basins = {}  # maps low point positions to the list of coords in the basin they occupy
    for lowpt in low_points:
        anim_basin = []  # provide a list to the scan function to capture coord list
        basins[lowpt] = exploreBasin(lowpt, basinmap, anim_basin=anim_basin)

        anim_coords.append(anim_basin)

    basin_sizes = {}  # maps low point positions to the size of the basin they occupy
    for lowpt in low_points:
        basin_sizes[lowpt] = len(basins[lowpt])

    # Convert basin_sizes into a sorted OrderedDict
    sorted_basin_sizes = OrderedDict(sorted(basin_sizes.items(), key=lambda t: t[1]))

    # Take out and format the top three basin sizes
    top3 = []
    for i in range(3):
        last = sorted_basin_sizes.popitem()
        top3.append( ((last[0].x, last[0].y), last[1]) )

    print(f"[Part 2] The three largest basins are {top3[0][1]} at {top3[0][0]}, {top3[1][1]} at {top3[1][0]}, and {top3[2][1]} at {top3[2][0]}, with a product of {top3[0][1]*top3[1][1]*top3[2][1]}.")


    ## Part 2 - Animation
    # Set lists and scaling factors for 400x400 and 800x800 frame sets
    frames_400 = []
    frames_800 = []
    anim_scale_400 = 4
    anim_scale_800 = 8

    # Set the (unscaled) frame size to match the initial heightmap image
    frame_size = img_heightmap.size

    # Set the initial (background) frames to the (scaled) previously generated height map
    init_frame_resized_400 = img_heightmap.resize((anim_scale_400*frame_size[0], anim_scale_400*frame_size[1]), resample=Image.NEAREST)
    init_frame_resized_800 = img_heightmap.resize((anim_scale_800*frame_size[0], anim_scale_800*frame_size[1]), resample=Image.NEAREST)
    frames_400.append(init_frame_resized_400)
    frames_800.append(init_frame_resized_800)

    # Make a sequence of colors to use for recently scanned pixels (the length of this list decides how many pixels should be tracked)
    # The leading pixel of a scanline will be the brightest, with the five next recently scanned positions progressively fading darker
    color_sequence = ['#00b80068', '#00a40032', '#006a0018', '#00580018', '#00480010', '#00380010']

    # Make a fixed-size queue for most-recently scanned pixels. The most recent pixel will be at the left end of the queue (use 'appendleft').
    last_scanned_pixels = deque([], len(color_sequence))

    # Create a frame for each pixel in the scan
    for basin in anim_coords:
        for pos in basin:
            frame = Image.new('RGBA', frame_size, ImageColor.getrgb('#00000000'))

            last_scanned_pixels.appendleft(pos)

            # Update any modified pixels for this frame
            for i, px in enumerate(last_scanned_pixels):
                frame.putpixel((px.x, px.y), ImageColor.getrgb(color_sequence[i]))

            frame_resized_400 = frame.resize((anim_scale_400*frame_size[0], anim_scale_400*frame_size[1]), resample=Image.NEAREST)
            frame_resized_800 = frame.resize((anim_scale_800*frame_size[0], anim_scale_800*frame_size[1]), resample=Image.NEAREST)
            frames_400.append(frame_resized_400)
            frames_800.append(frame_resized_800)

    # Save 400x400 APNGs
    frames_400[0].save('anim/day09_basinscan_400_slow.png', save_all=True, append_images=frames_400, default_image=True, disposal=0, blend=1, duration=50, loop=1)
    frames_400[0].save('anim/day09_basinscan_400_med.png', save_all=True, append_images=frames_400, default_image=True, disposal=0, blend=1, duration=30, loop=1)
    frames_400[0].save('anim/day09_basinscan_400_fast.png', save_all=True, append_images=frames_400, default_image=True, disposal=0, blend=1, duration=17, loop=1)

    # Save 800x800 APNGs
    frames_800[0].save('anim/day09_basinscan_800_slow.png', save_all=True, append_images=frames_800, default_image=True, disposal=0, blend=1, duration=50, loop=1)
    frames_800[0].save('anim/day09_basinscan_800_med.png', save_all=True, append_images=frames_800, default_image=True, disposal=0, blend=1, duration=30, loop=1)
    frames_800[0].save('anim/day09_basinscan_800_fast.png', save_all=True, append_images=frames_800, default_image=True, disposal=0, blend=1, duration=17, loop=1)
