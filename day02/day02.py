## Advent of Code 2021: Day 2
## https://adventofcode.com/2021/day/2
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 1714950, [Part 2]: 1281977850

import sys

class SubmarineMove():
    def __init__(self, initial_hpos=0, initial_depth=0):
        self.hpos = initial_hpos
        self.depth = initial_depth

    def _forward(self, steps=1):
        self.hpos += int(steps)   # increase horizontal position
    def _down(self, steps=1):
        self.depth += int(steps)  # increase depth
    def _up(self, steps=1):
        self.depth -= int(steps)  # decrease depth

    def doMove(self, move):
        if move[0] == 'forward': self._forward(move[1])
        elif move[0] == 'up': self._up(move[1])
        elif move[0] == 'down': self._down(move[1])
        else:
            print('Error: Invalid move.')
            sys.exit()

class SubmarineAim():
    def __init__(self, initial_hpos=0, initial_depth=0, initial_aim=0):
        self.hpos = initial_hpos
        self.depth = initial_depth
        self.aim = initial_aim

    def _forward(self, steps=1):
        self.hpos += int(steps)            # increase horizontal position
        self.depth += self.aim*int(steps)  # increase depth by a multiple of aim
    def _down(self, steps=1):
        self.aim += int(steps)  # increase aim
    def _up(self, steps=1):
        self.aim -= int(steps)  # decrease aim

    def doMove(self, move):
        if move[0] == 'forward': self._forward(move[1])
        elif move[0] == 'up': self._up(move[1])
        elif move[0] == 'down': self._down(move[1])
        else:
            print('Error: Invalid move.')
            sys.exit()

if __name__ == '__main__':
    with open('day02_input.txt', 'r') as f:
        def tupletize(line): return tuple( line.split() )
        course = list( map(tupletize, f.readlines()) )

    ## Part 1
    sub = SubmarineMove()

    for move in course:
        sub.doMove(move)

    print(f"[Part 1] Final horizontal position: {sub.hpos}. Final depth: {sub.depth}. Product: {sub.hpos*sub.depth}.")

    ## Part 2
    sub = SubmarineAim()

    for move in course:
        sub.doMove(move)

    print(f"[Part 2] Final horizontal position: {sub.hpos}. Final depth: {sub.depth}. Product: {sub.hpos*sub.depth}.")
