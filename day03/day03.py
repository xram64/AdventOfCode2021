## Advent of Code 2021: Day 3
## https://adventofcode.com/2021/day/3
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 3633500, [Part 2]: 4550283

import sys

# Return most commonly-found bit, breaking ties in favor of '1'
def get_most_common_bit(numbers, pos):
    frequency_of = [0, 0]  # frequencies for each bit [<0's>, <1's>]

    for num in numbers:
        if num[pos] == 0: frequency_of[0] += 1
        elif num[pos] == 1: frequency_of[1] += 1

    most_common_bit = 0 if (frequency_of[0] > frequency_of[1]) else 1
    return most_common_bit

# Return least commonly-found bit, breaking ties in favor of '0'
def get_least_common_bit(numbers, pos):
    return (get_most_common_bit(numbers, pos) ^ 1)


if __name__ == '__main__':
    with open('day03_input.txt', 'r') as f:
        def parse(line): return [int(bit) for bit in list(line) if (bit != '\n')]
        diag_numbers = list( map(parse, f.readlines()) )
    diag_numbers_len = len(diag_numbers[0])

    ##############
    ### Part 1 ###
    most_common_bits = ''
    for pos in range(diag_numbers_len):
        most_common_bits += str( get_most_common_bit(diag_numbers, pos) )

    # Epsilon rate: Most common bits from input
    ε = int(most_common_bits, 2)

    # Gamma rate: Least common bits from input
    γ = ε ^ int('1'*diag_numbers_len, 2)  # invert bits in ε

    print(f"[Part 1] Epsilon rate: ε = {ε}. Gamma rate: γ = {γ}. Power consumption: {ε*γ}.")

    ##############
    ### Part 2 ###
    oxy_rating_filtered_nums = diag_numbers
    co2_rating_filtered_nums = diag_numbers

    ## Oxygen generator rating
    for pos in range(diag_numbers_len):
        # Find most common bit (MCB) and filter numbers not matching bit criteria
        mcb = get_most_common_bit(oxy_rating_filtered_nums, pos)
        oxy_rating_filtered_nums = list( filter(lambda num: num[pos] == mcb, oxy_rating_filtered_nums) )

        if len(oxy_rating_filtered_nums) == 1:
            # Convert final element matching bit criteria to a decimal integer
            oxy_rating = int(''.join( [str(n) for n in oxy_rating_filtered_nums[0]] ), 2)
            break

        elif len(oxy_rating_filtered_nums) <= 0:
            print('Error: Oxygen rating list empty.')
            sys.exit()
    else:
        print('Error: Multiple numbers found matching bit criteria for oxygen rating.')
        sys.exit()

    ## CO2 scrubber rating
    for pos in range(diag_numbers_len):
        # Find least common bit (LCB) and filter numbers not matching bit criteria
        lcb = get_least_common_bit(co2_rating_filtered_nums, pos)
        co2_rating_filtered_nums = list( filter(lambda num: num[pos] == lcb, co2_rating_filtered_nums) )

        if len(co2_rating_filtered_nums) == 1:
            # Convert final element matching bit criteria to a decimal integer
            co2_rating = int(''.join( [str(n) for n in co2_rating_filtered_nums[0]] ), 2)
            break

        elif len(co2_rating_filtered_nums) <= 0:
            print('Error: CO2 rating list empty.')
            sys.exit()
    else:
        print('Error: Multiple numbers found matching bit criteria for CO2 rating.')
        sys.exit()


    print(f"[Part 2] Oxygen generator rating: {oxy_rating}. CO2 scrubber rating: {co2_rating}. Life support rating: {oxy_rating*co2_rating}.")
