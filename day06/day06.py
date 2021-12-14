## Advent of Code 2021: Day 6
## https://adventofcode.com/2021/day/6
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: , [Part 2]:

from time import time

DAYS = 256

def advance(age):
    # Returns a tuple with the new age of the current fish, followed by the
    #   age of a new fish if one should be spawned (otherwise, None)
    if age > 0:
        return (fish - 1, None)
    else:
        return (6, 8)

if __name__ == '__main__':

    t_start = time()

    with open('day06_input.txt', 'r') as f:
        fishesz = f.readline().split(',')
        fishes = [int(fish) for fish in fishesz]

    day = 0  # initial state
    for day in range(DAYS):
        print(f"Simulating day {day+1} (after {round(time() - t_start, 1)} seconds)...")
        new_fishes = []

        for i, fish in enumerate(fishes):
            fish, new_fish = advance(fish)
            fishes[i] = fish
            if new_fish:
                new_fishes.append(new_fish)

        fishes.extend(new_fishes)

        if day == (80-1):
            total_80d = len(fishes)

    total_256d = len(fishes)

    print(f"Ran in {time() - t_start} seconds.\n")

    print(f"[Part 1] After 80 days, there are {total_80d} lanternfish.")

    print(f"[Part 2] After 256 days, there are {total_256d} lanternfish.")
