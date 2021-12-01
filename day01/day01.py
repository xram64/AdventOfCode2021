## Advent of Code 2021: Day 1
## https://adventofcode.com/2021/day/1
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 1448, [Part 2]:

def count_increases(depths):
    increases = 0
    last_depth = None

    for depth in depths:
        if last_depth and (depth > last_depth):
            increases += 1
        last_depth = depth

    return increases

if __name__ == "__main__":
    depths = []
    with open('day01_input.txt', 'r') as f:
        for line in f.readlines():
            if line: depths.append( int(line) )

    ## Part 1
    increases = count_increases(depths)

    print(f"[Part 1] There are {increases} increased measurements.")


    ## Part 2
    window_sums = []

    for i in range(2, len(depths)):
        window_sums += [ depths[i-2] + depths[i-1] + depths[i] ]

    increases = count_increases(window_sums)

    print(f"[Part 2] There are {increases} increased measurements within three-measurement windows.")
