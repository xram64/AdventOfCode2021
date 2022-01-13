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


if __name__ == '__main__TEST':  ################################### TESTING ##########################################
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

###################################### TESTING ##########################################
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
    STEPS = 9
    flash_count = 0

    for t in range(STEPS):
        flash_count += advanceOctopi(octogrid)
        octogrid_states.append(octogrid.copy())
###################################### TESTING ##########################################


    ## Animation
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

    palette = {'A':'#015555', 'B':'#0a6e6e', 'C':'#1c8080', 'D':'#2b999a', 'E':'#2ea2a2', 'F':'#38b6b4'}

    colors = ['AAAABBBAAAAA', 'AABBBBBBBBAA', 'ABBBCCCCBBBA', 'ABCCCDDDFCBA', 'ABCDEEFFDCBA', 'ABCEEEEEECCA',
              'ABFEEEEEEDCA', 'BBCEEEEEDDCA', 'BBCEEEEFDCBA', 'ABBCEEEECCBA', 'ABBBBCCCCBBA', 'AABBBBBBAAAA']

    def paletteMap(color_string, palette):
        # Decodes a single row of palette data into RGB hex strings
        return [palette[color_letter] for color_letter in color_string]

    def generateBitmap(power_level, canvas_size, texture_colors, texture_palette, bg_color):
        # Returns an Image object with the texture for one octopus, scaled within its canvas based on power level

        texture_len = len(texture_colors)

        # Scaling factors, indexed by power level (0-9)
        POWER_SCALES = [3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]

        # Generate list of starting positions (in either direction) for each scaled pixel block
        # (Exploiting python's round() behavior to avoid bias in scaling directions for scale factors ending in 0.5!)
        boundary_coords = [round(POWER_SCALES[power_level]*i) for i in range(texture_len+1)]

        # Calculate final size (tuple) of scaled texture
        texture_scaled_size = (int(POWER_SCALES[power_level]*texture_len), )*2
        # Calculate offset (tuple) needed to center texture on canvas
        texture_scaled_offset = (int((canvas_size[0] - texture_scaled_size[0])/2), )*2


        # Create a flat list of pixel data for the texture bitmap
        octopus_flatbitmap = []

        # For each color in a row, add copies of it to the pixel data up to the next boundary to fill the scaled pixel area
        for i, color_row in enumerate(texture_colors):
            bitmap_row = []
            for color_pixel in [ImageColor.getrgb(c) for c in paletteMap(color_row, texture_palette)]:
                # Copy this pixel data as many times as the distance between the current and next boundary
                bitmap_row += [color_pixel]*(boundary_coords[i+1] - boundary_coords[i])
            # Also copy this entire row of pixel data as many times as the distance between the current and next boundary
            #  (to place multiple copies of this row and expand these pixels vertically)
            print(f"{boundary_coords[i+1] - boundary_coords[i]=}")
            for _ in range(boundary_coords[i+1] - boundary_coords[i]):
                print(f"{len(bitmap_row)=}")
                octopus_flatbitmap += bitmap_row

        # Create an uninitialized image object and copy in pixel data for the scaled texture
        texture = Image.new('RGB', texture_scaled_size, color=None)
        print(f"{boundary_coords=}")
        print(f"{texture_scaled_size=}")
        print(f"{len(octopus_flatbitmap)=}")
        texture.putdata(octopus_flatbitmap)

        # Create another image object the full size of the canvas and copy in texture data, centered on the canvas
        canvas = Image.new('RGB', canvas_size, color=ImageColor.getrgb(bg_color))
        canvas.paste(texture, box=texture_scaled_offset)
        return canvas


    # Squid textures are 12x12 px, so in a 10x10 grid with 2px padding, we get a total of (12*10)+(2*11) = 142px on each side
    # If squids are scaled to a full size of 96x96 px (each px scaled to cover 8px), we get (96*10)+(2*11) = 982px on each side,
    #   and we can scale squids in 5 steps, based on their power level:
    #   - [0-1]: (x4) 48x48
    #   - [2-3]: (x5) 60x60
    #   - [4-5]: (x6) 72x72
    #   - [6-7]: (x7) 84x84
    #   - [8-9]: (x8) 96x96

    # Squids can be scaled based on power level, with 48x48 squids for level 1 to 96x96 squids for level 9.
    # Odd-numbered squids can be directly scaled with each pixel occupying 4-8 pixels of the final image,
    #   but even-numbered squids must have scaling alternated.
    # For instance, the scale of each pixel of a power level 9 squid may be [8 8 8 8 8 8 8 8 8 8 8 8],
    #   but the scale of each pixel for a power level 8 squid will be [8 7 8 7 8 7 8 7 8 7 8 7].



    # Set lists and scaling factors
    frames = []
    frame_size = octogrid_states[0].shape
    anim_scale = 4
    c_BG = '#3a3a3a'  # default background color

    i = 0####TEST

    # Create a frame for each step in the grid state history
    for octogrid in octogrid_states:
        frame = Image.new('RGB', frame_size, ImageColor.getrgb(c_BG))

        # For each octopus in the grid, create a flattened array of 96x96 pixel color data,
        #   depending on the current power level of the octopus.
        octopus_iter = np.nditer(octogrid, flags=['multi_index'])
        for power_level in octopus_iter:

            # Find coords of top-left corner of the location for this octopus in the image
            topleft_coords = (0,0)####TEST

            # Generate the image object for this octopus (depending on power level)
            octopus_bitmap = generateBitmap(i, (96, 96), colors, palette, c_BG)

            # Add this octopus to the frame
            # frame.paste(octopus_bitmap, topleft_coords)
        # frame.save(f'test{i}.png') #### TEST ####

        #### TEST ####
        # octopus_bitmap = octopus_bitmap.resize((8*12, 8*12), resample=Image.NEAREST)
        octopus_bitmap.save(f'test{i}.png')
        i += 1
        #### TEST ####


        # # Update any modified pixels for this frame
        # for i, px in enumerate(last_scanned_pixels):
        #     frame.putpixel((px.x, px.y), ImageColor.getrgb(color_sequence[i]))
        #
        # frame_resized = frame.resize((anim_scale*frame_size[0], anim_scale*frame_size[1]), resample=Image.NEAREST)
        # frames.append(frame_resized)

    # Save APNGs
    # frames[0].save('anim/day11_octogrid_slow.png', save_all=True, append_images=frames, default_image=True, disposal=0, blend=1, duration=50, loop=1)
    # frames[0].save('anim/day11_octogrid_fast.png', save_all=True, append_images=frames, default_image=True, disposal=0, blend=1, duration=17, loop=1)
