## Advent of Code 2021: Day 10
## https://adventofcode.com/2021/day/10
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 311949, [Part 2]: 3042730309

from collections import namedtuple, deque
from enum import Enum, auto
from math import ceil

Bounds = namedtuple('Bounds', ['left', 'right'])

class Status(Enum):
    Corrupted = auto()
    Incomplete = auto()
    Valid = auto()

corrupted_char_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
incomplete_char_score = {')': 1, ']': 2, '}': 3, '>': 4}

char_pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
open_chars = list(char_pairs.keys())
close_chars = list(char_pairs.values())


def getLineScore(chars):
    global incomplete_char_score
    score = 0
    for char in chars:
        score *= 5
        score += incomplete_char_score[char]
    return score


if __name__ == '__main__':
    with open('day10_input.txt', 'r') as f:
        lines = f.readlines()

    # For each line, track whether the line is corrupted, incomplete, or valid
    line_status = []
    # Save first corrupted char on each corrupted line, indexed by line number
    corrupted_chars = {}
    # Save leftover unmatched chars on each incomplete line, indexed by line number
    incomplete_chars = {}

    ## Part 1
    for n, line in enumerate(lines):
        chars = list(line.strip())

        unmatched_chars = deque()

        # Scan through chars on the line and check for bracket matches
        for char in chars:
            # If we get an open bracket, push onto stack
            if char in open_chars:
                unmatched_chars.append(char)

            # If we get a close bracket, check if it matches the last open bracket
            # (Assuming here that we won't run into more closing brackets than open brackets)
            elif char in close_chars:
                # If the close bracket matches the last open bracket, this chunk is valid, so pop the bracket off the stack and continue
                if char == char_pairs[unmatched_chars[-1]]:
                    unmatched_chars.pop()

                # If paired brackets don't match, this is a corrupted line
                else:
                    line_status.append(Status.Corrupted)
                    corrupted_chars[n] = char
                    break

        else:
            # At the end of the line, if we still have unmatched chars, the line must be incomplete
            if len(unmatched_chars) > 0:
                line_status.append(Status.Incomplete)

                # Store the remaining, unmatched chars for this line
                incomplete_chars[n] = unmatched_chars

            # Otherwise, the line is valid
            else:
                line_status.append(Status.Valid)

    syntax_error_score = sum( [corrupted_char_score[c] for c in corrupted_chars.values()] )

    print(f"[Part 1] Out of {len(lines)} lines, {line_status.count(Status.Corrupted)} are corrupted, {line_status.count(Status.Incomplete)} are incomplete, and {line_status.count(Status.Valid)} are valid. The total syntax error score is {syntax_error_score}.")


    ## Part 2
    # Keep track of the final total score for each incomplete line
    line_scores = []

    for chars in list(incomplete_chars.values()):
        # Map each opening bracket in the reversed set of uncompleted chars to its corresponding closing bracket
        rev_chars = chars.copy()
        rev_chars.reverse()

        completed_chars = []
        for char in rev_chars:
            completed_chars.append(char_pairs[char])

        line_scores.append( getLineScore(completed_chars) )

    middle_score = sorted(line_scores)[ceil(len(line_scores)/2) - 1]

    print(f"[Part 2] The middle score for incomplete lines is {middle_score}.")
