## Advent of Code 2021: Day 11
## https://adventofcode.com/2021/day/11
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 1741, [Part 2]: 440

import numpy as np
from PIL import Image, ImageColor

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
    # Handles one step for all octopi in the grid, returning the set of octopi that flashed this step:
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

    return flashed


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
        flashes = advanceOctopi(octogrid)
        flash_count += len(flashes)
        octogrid_states.append(octogrid.copy())

    print(f"[Part 1] After 100 steps, a total of {flash_count} octopus flashes occurred.")


    ## Part 2
    step_count = 0
    flash_count = 0

    # Reset grid to initial state
    octogrid = octogrid_states[0].copy()
    octogrid_states = []
    octogrid_states.append(octogrid.copy())  # t = 0

    # Keep a parallel list to octogrid_states tracking the positions of the octopi that flashed on each step,
    #   initialized with an empty set to match the initial grid state.
    flash_positions_by_state = [set()]

    octopi_synchronized = False
    while not octopi_synchronized:
        step_count += 1

        flashes = advanceOctopi(octogrid)
        flash_count += len(flashes)

        octogrid_states.append(octogrid.copy())
        flash_positions_by_state.append(flashes)

        # If there were as many flashes as octopi in the grid, they all must have flashed simultaneously.
        if len(flashes) == octogrid.size:
            octopi_synchronized = True

    print(f"[Part 2] All octopi flash simultaneously on step {step_count}, after a total of {flash_count} flashes.")



    ###############
    ## Animation ##
    ###############

    # Glow squid color map (top-back to top-front):
    #  [Row 1]  |#015555 #015555 #015555 #015555|#0a6e6e #0a6e6e #0a6e6e|#015555 #015555 #015555 #015555 #015555|
    #  [Row 2]  |#015555 #015555|#0a6e6e #0a6e6e #0a6e6e #0a6e6e #0a6e6e #0a6e6e #0a6e6e #0a6e6e|#015555 #015555|
    #  [Row 3]  |#015555|#0a6e6e #0a6e6e #0a6e6e|#1c8080 #1c8080 #1c8080 #1c8080|#0a6e6e #0a6e6e #0a6e6e|#015555|
    #  [Row 4]  |#015555|#0a6e6e|#1c8080 #1c8080 #1c8080|#2b999a #2b999a #2b999a|#38b6b4|#1c8080|#0a6e6e|#015555|
    #  [Row 5]  |#015555|#0a6e6e|#1c8080|#2b999a|#2ea2a2 #2ea2a2|#38b6b4 #38b6b4|#2b999a|#1c8080|#0a6e6e|#015555|
    #  [Row 6]  |#015555|#0a6e6e|#1c8080|#2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2|#1c8080 #1c8080|#015555|
    #  [Row 7]  |#015555|#0a6e6e|#38b6b4|#2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2|#2b999a|#1c8080|#015555|
    #  [Row 8]  |#0a6e6e #0a6e6e|#1c8080|#2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2|#2b999a #2b999a|#1c8080|#015555|
    #  [Row 9]  |#0a6e6e #0a6e6e|#1c8080|#2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2|#38b6b4|#2b999a|#1c8080|#0a6e6e|#015555|
    # [Row 10]  |#015555|#0a6e6e #0a6e6e|#1c8080|#2ea2a2 #2ea2a2 #2ea2a2 #2ea2a2|#1c8080 #1c8080|#0a6e6e|#015555|
    # [Row 11]  |#015555|#0a6e6e #0a6e6e #0a6e6e #0a6e6e|#1c8080 #1c8080 #1c8080 #1c8080|#0a6e6e #0a6e6e|#015555|
    # [Row 12]  |#015555 #015555|#0a6e6e #0a6e6e #0a6e6e #0a6e6e #0a6e6e #0a6e6e|#015555 #015555 #015555 #015555|

    base_palette = {'A':'#015555', 'B':'#0a6e6e', 'C':'#1c8080', 'D':'#2b999a', 'E':'#2ea2a2', 'F':'#38b6b4'}      # default
    flashLo_palette = {'A':'#007270', 'B':'#009897', 'C':'#00b9b8', 'D':'#00d2d2', 'E':'#06d6d6', 'F':'#0ad6d6'}   # low flash
    flashHi_palette = {'A':'#00b1b0', 'B':'#00d4d2', 'C':'#00d4d2', 'D':'#00dada', 'E':'#0cdcdc', 'F':'#12dcdc'}   # high flash
    # flashLo_palette = {'A':'#008b89', 'B':'#00b1b0', 'C':'#00cdcb', 'D':'#00f4f4', 'E':'#10ffff', 'F':'#19ffff'}   # low flash (brighter)
    # flashHi_palette = {'A':'#00c5c3', 'B':'#00faf8', 'C':'#00fefb', 'D':'#00ffff', 'E':'#10ffff', 'F':'#27ffff'}   # high flash (brighter)

    colors = ['AAAABBBAAAAA', 'AABBBBBBBBAA', 'ABBBCCCCBBBA', 'ABCCCDDDFCBA', 'ABCDEEFFDCBA', 'ABCEEEEEECCA',
              'ABFEEEEEEDCA', 'BBCEEEEEDDCA', 'BBCEEEEFDCBA', 'ABBCEEEECCBA', 'ABBBBCCCCBBA', 'AABBBBBBAAAA']

    def paletteMap(color_string, palette):
        # Decodes a single row of palette data into RGB hex strings
        return [palette[color_letter] for color_letter in color_string]

    def getCornerCoordsInFrame(octopus_position, canvas_size, padding):
        # Calculate the upper-left corner position for an octopus in the final image, with the given
        #   size of the octopus texture (canvas_size) and padding.
        y_coord = padding*(octopus_position[0]+1) + canvas_size[0]*octopus_position[0]
        x_coord = padding*(octopus_position[1]+1) + canvas_size[0]*octopus_position[1]
        return (x_coord, y_coord)

    def generateBitmap(power_level, canvas_size, texture_colors, texture_palette, bg_color):
        # Returns an Image object with the texture for one octopus, scaled within its canvas based on power level
        # All images returned by this function will have dimensions of 'canvas_size'.

        # Get dimensions of the base texture (taken from the color data)
        texture_size = (len(texture_colors), )*2

        # Scaling factors, indexed by power level (0-9)
        # POWER_SCALES = [(i+1)/20+0.5 for i in range(10)]  # [0.55, ..., 1.0]
        POWER_SCALES = [(i+1)/32+0.6875 for i in range(10)]  # [0.71875, ..., 1.0]

        # Create a flat list of pixel data for the texture bitmap
        octopus_flatbitmap = []

        # Copy the pixel data (as RGB tuples) into the bitmap for each row of the texture
        for color_row in texture_colors:
            octopus_flatbitmap += [ImageColor.getrgb(c) for c in paletteMap(color_row, texture_palette)]

        # Create an uninitialized image object and copy in pixel data for the unscaled texture
        texture = Image.new('RGB', texture_size, color=None)
        texture.putdata(octopus_flatbitmap)

        # Scale the texture based on its power level
        texture_scaled_size = (round(POWER_SCALES[power_level] * canvas_size[0]), )*2
        texture = texture.resize(texture_scaled_size, resample=Image.NEAREST)

        # Calculate offset for texture within the canvas (always rounded down)
        texture_scaled_offset = int( (canvas_size[0] - texture_scaled_size[0])/2 )

        # Create another image object the full size of the canvas and copy in texture data, centered on the canvas
        canvas = Image.new('RGB', canvas_size, color=ImageColor.getrgb(bg_color))
        canvas.paste(texture, box=(texture_scaled_offset, texture_scaled_offset))
        return canvas


    # Squid textures are 12x12 px, so in a 10x10 grid with 2px padding, we get a total of (12*10)+(2*11) = 142px on each side
    # If squids are scaled to a full size of 96x96 px (each px scaled to cover 8px), we get (96*10)+(2*11) = 982px on each side,
    #   and we can scale squids in steps, based on their power level.

    # Set lists and scaling factors
    frames = []
    frame_durations = [50]  # duration of each frame, starting with the duration of the extra 'default_image' frame
    canvas_size = (96, 96)  # space in final image for each octopus
    octogrid_size = octogrid_states[0].shape
    frame_padding = 4
    frame_size = ( canvas_size[0]*octogrid_size[0] + (frame_padding*(octogrid_size[0]+1)),
                   canvas_size[1]*octogrid_size[1] + (frame_padding*(octogrid_size[0]+1)) )

    c_BG = '#242424'  # default background color
    DUR_NOFLASH = 220    # duration of a regular frame that does not follow a flashing frame  [fast: 150 / slow: 220]
    DUR_PREFLASH = 40    # duration of a regular frame that follows a flashing frame          [fast:  30 / slow:  40]
    DUR_FLASHING = 60    # duration of a flashing frame (3x per regular frame)                [fast:  40 / slow:  60]

    # Create a frame for each step in the grid state history
    for step, octogrid in enumerate(octogrid_states):
        frame = Image.new('RGB', frame_size, ImageColor.getrgb(c_BG))

        # For each octopus in the grid, create a flattened array of 96x96 pixel color data,
        #   depending on the current power level of the octopus.
        octopus_iter = np.nditer(octogrid, flags=['multi_index'])
        for power_level in octopus_iter:

            # Find coords of top-left corner of the location for this octopus in the image
            topleft_coords = getCornerCoordsInFrame(octopus_iter.multi_index, canvas_size, frame_padding)

            # Generate the image object for this octopus (depending on power level)
            octopus_bitmap = generateBitmap(power_level, (96, 96), colors, base_palette, c_BG)

            # Add this octopus to the frame
            frame.paste(octopus_bitmap, topleft_coords)

        # If any octopi flashed on the last step, generate three extra 'flash' frames to insert before the regular frame for this step.
        if len(flash_positions_by_state[step]) > 0:

            # Override the last duration value to be a "pre-flash" duration
            frame_durations[-1] = DUR_PREFLASH

            # Make a queue of palettes for each 'flash' frame
            next_palettes = [flashLo_palette, flashHi_palette, flashLo_palette]
            for next_palette in next_palettes:
                flash_frame = Image.new('RGB', frame_size, ImageColor.getrgb(c_BG))

                # Get the power levels for this 'flash' frame from the previous step (where these octopi were flashing)
                octopus_iter = np.nditer(octogrid_states[step-1], flags=['multi_index'])
                for power_level in octopus_iter:

                    # Find coords of top-left corner of the location for this octopus in the image
                    topleft_coords = getCornerCoordsInFrame(octopus_iter.multi_index, canvas_size, frame_padding)

                    # Generate a 'flash' bitmap for any flashing octopi and a regular bitmap for the rest
                    if octopus_iter.multi_index in flash_positions_by_state[step]:
                        octopus_bitmap = generateBitmap(power_level, (96, 96), colors, next_palette, c_BG)
                    else:
                        octopus_bitmap = generateBitmap(power_level, (96, 96), colors, base_palette, c_BG)

                    # Add this octopus to the 'flash' frame
                    flash_frame.paste(octopus_bitmap, topleft_coords)

                # Add the 'flash' frame to the frame list (before the regular frame for this step)
                frames.append(flash_frame)
                frame_durations.append(DUR_FLASHING)


        # Add the final image for this step to the frame list (after the 'flash' frame has been added, if any)
        frames.append(frame)
        frame_durations.append(DUR_NOFLASH)  # assume this will be a full-length frame, unless overridden by a flashing frame in the next step


    # Save APNGs (leave off last all-0 frame)
    frames[0].save('anim/day11_octogrid_slow.png', save_all=True, append_images=frames[:-1], default_image=True, disposal=0, blend=1, duration=frame_durations[:-1], loop=1)
