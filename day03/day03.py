## Advent of Code 2021: Day 3
## https://adventofcode.com/2021/day/3
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 3633500, [Part 2]:

import sys

def get_most_common_bit(numbers, pos):
    # Find the most common bit (0 or 1) in position 'pos' of each number in 'numbers'
    frequency_of = [0, 0]  # frequencies for each bit [<0's>, <1's>]

    for num in numbers:
        if num[pos] == 0: frequency_of[0] += 1
        elif num[pos] == 1: frequency_of[1] += 1

    most_common_bit = 0 if (frequency_of[0] > frequency_of[1]) else 1
    return most_common_bit

if __name__ == '__main__':
    with open('day03_input.txt', 'r') as f:
        def parse(line): return [int(bit) for bit in list(line) if (bit != '\n')]
        diag_numbers = list( map(parse, f.readlines()) )
    diag_numbers_len = len(diag_numbers[0])


    ## Part 1
    most_common_bits = ''
    for pos in range(diag_numbers_len):
        most_common_bits += str( get_most_common_bit(diag_numbers, pos) )

    # Epsilon rate: Most common bits from input
    ε = int(most_common_bits, 2)

    # Gamma rate: Least common bits from input
    γ = ε ^ int('1'*diag_numbers_len, 2)  # XOR with 111111111111

    print(f"[Part 1] Epsilon rate: ε = {ε}. Gamma rate: γ = {γ}. Power consumption: {ε*γ}.")


    ## Part 2
    # for i in range(diag_numbers_len):
    #     # Filter numbers
    #     filter( (lambda num: num[i] > ), diag_numbers )
