## Advent of Code 2021: Day 11
## https://adventofcode.com/2021/day/11
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 1741, [Part 2]: 440

import numpy as np

def getAdjacent(pos):
    # Returns all valid adjacent positions (cardinal and diagonal) to the given position tuple
    adjacent = set()

    for r in range(-1, 2):
        for c in range(-1, 2):
            # Add all points in 3x3 grid around 'pos', skipping any points outside boundary
            if (0 <= pos[0]+r <= 9) and (0 <= pos[1]+c <= 9):
                adjacent.add( (pos[0]+r, pos[1]+c) )

    # Remove point at 'pos'
    adjacent.discard( pos )

    return list(adjacent)


def advanceOctopi(octogrid):
    # Handles one step for all octopi in the grid, returning the new grid state:
    #  (1)  Increase energy level of all octopi by 1.
    #  (2)  Check if any octopus has reached an energy level > 9, entering the 'flash' state.
    #       Octopi that have already entered the 'flash' state on this step are ignored.
    #  (3)  Increase the power level of all octopi adjacent (including diagonally) to any octopus
    #       that just entered the 'flash' state.
    #  (4)  Repeat (2) and (3) until no new 'flash' state transitions occur.
    #  (5)  Reset all octopi with energy level > 9 to level 0.

    # Set of indices for octopi that have already flashed on this step.
    flashed = set()

    #  (1)
    octogrid += np.ones_like(octogrid)

    #  (2)-(4)
    new_flashes = True  # flag to end loop when no new flashes have occured
    while new_flashes:
        new_flashes = False
        octopus_iter = np.nditer(octogrid, flags=['multi_index'])

        for power_level in octopus_iter:
            octopus = octopus_iter.multi_index  # grid position for this octopus

            if power_level > 9:  # it's over 9(000)!
                if octopus not in flashed:
                    new_flashes = True
                    flashed.add(octopus)

                    octopus_friends = getAdjacent(octopus)
                    for friend in octopus_friends:
                        octogrid[friend] += 1

    #  (5)
    octogrid[octogrid > 9] = 0

    return len(flashed)


if __name__ == '__main__':
    with open('day11_input.txt', 'r') as f:
        lines = f.readlines()

    # List to keep track of the state history of the grid
    octogrid_states = []

    str_octogrid = [list(line.strip()) for line in lines]

    # Initialize grid and add initial state to history list
    octogrid = np.array(str_octogrid, dtype=np.int8)
    octogrid_states.append(octogrid.copy())  # t = 0


    ## Part 1
    STEPS = 100
    flash_count = 0

    for t in range(STEPS):
        flash_count += advanceOctopi(octogrid)
        octogrid_states.append(octogrid.copy())

    print(f"[Part 1] After 100 steps, a total of {flash_count} octopus flashes occurred.")


    ## Part 2
    step_count = 0
    flash_count = 0

    # Reset grid to initial state
    octogrid = octogrid_states[0].copy()
    octogrid_states = []

    octopi_synchronized = False
    while not octopi_synchronized:
        step_count += 1

        flashes = advanceOctopi(octogrid)
        flash_count += flashes

        octogrid_states.append(octogrid.copy())

        # If there were as many flashes as octopi in the grid, they all must have flashed simultaneously.
        if flashes == octogrid.size:
            octopi_synchronized = True

    print(f"[Part 2] All octopi flash simultaneously on step {step_count}, after a total of {flash_count} flashes.")
