## Advent of Code 2021: Day 7
## https://adventofcode.com/2021/day/7
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 329389, [Part 2]: 86397080

from sys import maxsize as MAXINT
from functools import reduce

def triangleSum(n):
    # https://en.wikipedia.org/wiki/Triangular_number
    # Σ_n{k} = n(n+1)/2
    return int(n*(n+1)/2)

if __name__ == '__main__':
    with open('day07_input.txt', 'r') as f:
        positions = [int(i) for i in f.readline().split(',')]

    # Ci:  The ith constant from the list of initial horizontal positions, {C1, ..., Cn}
    # x:   A variable representing the target final horizontal position
    # S:   A function of x representing the sum over all differences in initial/final positions
    # S(x)  =  Σ|Ci - x|  =  |C1 - x| + |C2 - x| + ... + |Cn - x|


    ## Part 1
    positions_sorted = sorted(positions)

    pos_min = positions_sorted[0]
    pos_max = positions_sorted[-1]

    minimum = (0, MAXINT)  # (target position, total fuel consumed)

    for final_pos in range(pos_min, pos_max+1):
        pos_changes = map(lambda pos: abs(pos - final_pos), positions)
        total_fuel = sum(pos_changes)

        if (total_fuel < minimum[1]):
            minimum = (final_pos, total_fuel)

    print(f"[Part 1] Final horizontal position: {minimum[0]}. Total fuel consumed: {minimum[1]}.")


    ## Part 2
    minimum = (0, MAXINT)  # (target position, total fuel consumed)

    for final_pos in range(pos_min, pos_max+1):
        pos_changes = map(lambda pos: triangleSum(abs(pos - final_pos)), positions)
        total_fuel = sum(pos_changes)

        if (total_fuel < minimum[1]):
            minimum = (final_pos, total_fuel)

    print(f"[Part 2] Final horizontal position: {minimum[0]}. Total fuel consumed: {minimum[1]}.")
