## Advent of Code 2021: Day 3
## https://adventofcode.com/2021/day/3
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: , [Part 2]:

import sys

if __name__ == '__main__':
    with open('day03_input.txt', 'r') as f:
        def parse(line): return [int(bit) for bit in list(line) if (bit != '\n')]
        diag_numbers = list( map(parse, f.readlines()) )

    number_length = len(diag_numbers[0])

    # Dictionary containing frequencies of 0's and 1's in each position
    # For each entry, the key is the bit position and the value is a tuple
    #  with the format: (<count of 0's>, <count of 1's>).
    frequencies = {}
    for i in range(number_length):
        frequencies[i] = (0, 0)  # initialize counts in dictionary

    for number in diag_numbers:
        for pos, bit in enumerate(number):
            if bit == 0:
                frequencies[pos] = (frequencies[pos][0]+1, frequencies[pos][1])
            elif bit == 1:
                frequencies[pos] = (frequencies[pos][0], frequencies[pos][1]+1)
            else:
                print('Error: Invalid digit.')
                sys.exit()

    most_common_bits = ''
    for i in range(number_length):
        # Append 0 if there are more 0's than 1's in this position, otherwise append 1
        most_common_bits += '0' if (frequencies[i][0] > frequencies[i][1]) else '1'

    # Epsilon rate: Most common bits from input
    ε = int(most_common_bits, 2)

    # Gamma rate: Least common bits from input
    γ = ε ^ int('1'*number_length, 2)  # XOR with 111111111111

    print(f"[Part 1] Epsilon rate: ε = {ε}. Gamma rate: γ = {γ}. Power consumption: {ε*γ}.")
