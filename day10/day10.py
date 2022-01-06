## Advent of Code 2021: Day 10
## https://adventofcode.com/2021/day/10
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 311949, [Part 2]:

from collections import namedtuple, deque
from enum import Enum, auto

Bounds = namedtuple('Bounds', ['left', 'right'])

class Status(Enum):
    Corrupted = auto()
    Incomplete = auto()
    Valid = auto()

illegal_char_score = {')': 3, ']': 57, '}': 1197, '>': 25137}

char_pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
open_chars = list(char_pairs.keys())
close_chars = list(char_pairs.values())


if __name__ == '__main__':
    with open('day10_input.txt', 'r') as f:
        lines = f.readlines()

    # For each line, track whether the line is corrupted, incomplete, or valid
    line_status = []
    # First corrupted char on each corrupted line, indexed by line number
    corrupted_chars = {}

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

            # Otherwise, the line is valid
            else:
                line_status.append(Status.Valid)

    syntax_error_score = sum( [illegal_char_score[c] for c in corrupted_chars.values()] )

    print(f"[Part 1] Out of {len(lines)} lines, {line_status.count(Status.Corrupted)} are corrupted, {line_status.count(Status.Incomplete)} are incomplete, and {line_status.count(Status.Valid)} are valid. The total syntax error score is {syntax_error_score}.")

    ## Part 2





### First draft
#
# def parseChunk():
#     ...
#
# class Chunk():
#     def __init__(self, chars, isCorrputed):
#         self.chars = deque(chars)
#         self.isCorrputed = isCorrputed
#
#
# if __name__ == '__main__':
#     with open('test_input.txt', 'r') as f:
#         lines = f.readlines()
#         print(lines)
#
#     # List of Chunk objects for each line
#     chunks = []
#
#     TEST = []
#
#     for line in lines:
#         chars = list(line.strip())
#
#         chunks_in_line = []
#         bnd_left = 0
#         depth = 0
#
#         for i, char in enumerate(chars):
#             if char in open_chars:
#                 depth += 1
#             elif char in close_chars:
#                 depth -= 1
#
#             TEST.append(depth)
#
#             # Once the depth returns to 0
#             if depth == 0:
#                 bnds = Bounds(bnd_left, i)
#                 bnd_left = i
#
#                 # If the start of this "chunk" isn't a valid open char, mark line as corrupted
#                 if not chars[bnds.left] in open_chars:
#                     chunks_in_line.append( Chunk(chars[bnds.left:bnds.right+1], isCorrputed=True) )
#
#                 # If the ends of chars at the same depth don't match, mark line as corrupted
#                 elif char_pairs[chars[bnds.left]] != chars[bnds.right]:
#                     chunks_in_line.append( Chunk(chars[bnds.left:bnds.right+1], isCorrputed=True) )
#
#                 else:
#                     chunks_in_line.append( Chunk(chars[bnds.left:bnds.right+1], isCorrputed=False) )
#
#
#         else:
#             # If the depth doesn't return to 0 at the end of a line, the line is incomplete
#             if depth != 0:
#                 chunks.append(chunks_in_line)
#
#             # Otherwise, this is a complete line, so we'll save the chunks
#             else:
#                 chunks.append(chunks_in_line)
#
#             TEST.append('--------')
#
#     print(TEST)
#
#
#     for line in chunks:
#         for chunk in line:
#             print(chunk.chars)
#             print(chunk.isCorrputed)
