## Advent of Code 2021: Day 8
## https://adventofcode.com/2021/day/8
## Jesse Williams | github.com/xram64
## Answers: [Part 1]: 470, [Part 2]: 989396

from enum import Enum, auto

## Digits by number of lit segments:
#  2 segments: 1
#  3 segments: 7
#  4 segments: 4
#  5 segments: 2, 3, 5
#  6 segments: 0, 6, 9
#  7 segments: 8

## Segment names:
#  a = N    (north)
#  b = NW   (northwest)
#  c = NE   (northeast)
#  d = C    (center)
#  e = SW   (southwest)
#  f = SE   (southeast)
#  g = S    (south)
#
#    aaaa    =     NNNN
#   b    c   =   NW    NE
#   b    c   =   NW    NE
#    dddd    =     CCCC
#   e    f   =   SW    SE
#   e    f   =   SW    SE
#    gggg    =     SSSS

## Heuristics:
# —{1}— The 2-seg number ('1') identifies NE and SE, but does not distinguish them.
# —{2}— Of the three 6-seg numbers, one of them will be missing one of the two letters from the 2-seg number.
#     The missing letter must correspond to NE, and the other letter from the 2-seg number must be SE.
#     Also, the 6-seg number with the missing letter must be '6'.
# —{3}— All 5-seg numbers can now be identified by comparing present or missing NE/SE segments.
#    · '5' is missing NE
#    · '2' is missing SE
#    · '3' includes both NE and SE
# —{4}— The 3-seg number ('7') identifies N by the letter that is not NE or SE.
# —{5}— The 4-seg number ('4') identifies NW and C by the letters that are not NE or SE. These letters can then be
#     distinguished by finding the one that does not appear in '3' (or '2'), which must be NW. The other
#     letter must then be C.
# —{6}— The remaining 6-seg numbers ('0' and '9') can now be identified by comparing present or missing C segments.
#    · '0' is missing C
#    · '9' includes C
# —{7}— The letter that '9' is missing compared to '8' (the 8-seg number) must be SW.
# —{8}— The only remaining unidentified letter must be S.


class Seg(Enum):
    N = auto()
    NW = auto()
    NE = auto()
    C = auto()
    SW = auto()
    SE = auto()
    S = auto()

ALL_SEGMENTS = {Seg.N, Seg.NW, Seg.NE, Seg.C, Seg.SW, Seg.SE, Seg.S}

DIGIT_0 = ALL_SEGMENTS - {Seg.C}
DIGIT_1 = {Seg.NE, Seg.SE}
DIGIT_2 = ALL_SEGMENTS - {Seg.NW, Seg.SE}
DIGIT_3 = ALL_SEGMENTS - {Seg.NW, Seg.SW}
DIGIT_4 = {Seg.NE, Seg.SE, Seg.NW, Seg.C}
DIGIT_5 = ALL_SEGMENTS - {Seg.NE, Seg.SW}
DIGIT_6 = ALL_SEGMENTS - {Seg.NE}
DIGIT_7 = {Seg.NE, Seg.SE, Seg.N}
DIGIT_8 = ALL_SEGMENTS
DIGIT_9 = ALL_SEGMENTS - {Seg.SW}
DIGIT = [DIGIT_0, DIGIT_1, DIGIT_2, DIGIT_3, DIGIT_4, DIGIT_5, DIGIT_6, DIGIT_7, DIGIT_8, DIGIT_9]


class Display():
    def __init__(self, tests, outputs):
        self.outputs = outputs
        self.output_digits = None

        # Fill a dict with the letter sequences for each length of segment string
        letter_sequences = {2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
        for test in tests:
            letter_sequences[len(test)].append(test)

        # Final determined segments
        segments = {}
        # Discovered digits corresponding to each letter string
        digits = {}


        ##| —{1}— |##
        digits['1'] = set(letter_sequences[2][0])

        ##| —{2}— |##
        for seq in letter_sequences[6]:
            if (digits['1'] - set(seq)) != set():
                # If we don't get an empty set, this sequence must be 6
                digits['6'] = set(seq)
                # We can identify NE by the remaining letter after subtracting '6'
                segments[Seg.NE] = list(digits['1'] - set(seq))[0]
                # We can identify SE by the other letter from '1'
                segments[Seg.SE] = list(digits['1'] - set(segments[Seg.NE]))[0]
                break

        ##| —{3}— |##
        for seq in letter_sequences[5]:
            if (segments[Seg.NE] in seq) and (segments[Seg.SE] in seq):
                digits['3'] = set(seq)
            elif (segments[Seg.NE] in seq):
                digits['2'] = set(seq)
            elif (segments[Seg.SE] in seq):
                digits['5'] = set(seq)

        ##| —{4}— |##
        digits['7'] = set(letter_sequences[3][0])
        segments[Seg.N] = list(digits['7'] - digits['1'])[0]

        ##| —{5}— |##
        digits['4'] = set(letter_sequences[4][0])
        segments[Seg.NW] = list(digits['4'] - digits['3'])[0]
        segments[Seg.C] = list(digits['4'] - digits['1'] - set(segments[Seg.NW]))[0]

        ##| —{6}— |##
        for seq in letter_sequences[6]:
            if set(seq) == digits['6']:
                pass  # we've already identified the '6'
            elif segments[Seg.C] in seq:
                digits['9'] = set(seq)
            elif segments[Seg.C] not in seq:
                digits['0'] = set(seq)

        ##| —{7}— |##
        digits['8'] = set(letter_sequences[7][0])
        segments[Seg.SW] = list(digits['8'] - digits['9'])[0]

        ##| —{8}— |##
        # Removing all determined segment letters from '8', we're left with the S segment
        segments[Seg.S] = list(digits['8'] - set(segments.values()))[0]

        # Save letters corresponding to each segment for this display
        self.N = segments[Seg.N]
        self.NW = segments[Seg.NW]
        self.NE = segments[Seg.NE]
        self.C = segments[Seg.C]
        self.SW = segments[Seg.SW]
        self.SE = segments[Seg.SE]
        self.S = segments[Seg.S]

        # Create lookup dict for letters corresponding to their segment
        self.segmentFor = {self.N: Seg.N, self.NW: Seg.NW, self.NE: Seg.NE, self.C: Seg.C, self.SW: Seg.SW, self.SE: Seg.SE, self.S: Seg.S}


    def _parseOutputNumbers(self):
        # Returns a list of the numbers found in the output
        output_digits = []

        # Check each digit in 4-digit output number
        for digit_letters in self.outputs:

            # Scan through letters within number, collecting the corresponding segments
            segs = set()
            for letter in digit_letters:
                segs |= {self.segmentFor[letter]}

            # Identify the digit that contains these segments
            for n, DIG in enumerate(DIGIT):
                if DIG == segs:
                    output_digits.append(n)
                    break

        self.output_digits = output_digits

    def getOutputNumbers(self):
        if not self.output_digits:
            # If we haven't already parsed the numbers, do it now
            self._parseOutputNumbers()
            return self.output_digits
        else:
            # Otherwise, return the stored numbers
            return self.output_digits


    def formatOutputNumbers(self):
        # Returns a formatted visual display of all 4 output numbers
        digits = self.getOutputNumbers()

        formatted_numbers_separated = []
        formatted_numbers_full = ["", "", "", "", ""]

        for n in digits:
            # Format display strings
            display_lines = ["   ", "   ", "   ", "   ", "   "]
            if Seg.N in DIGIT[n]:
                display_lines[0] = "###"
            if Seg.NW in DIGIT[n]:
                display_lines[1] = "#" + display_lines[1][1:]
            if Seg.NE in DIGIT[n]:
                display_lines[1] = display_lines[1][:2] + "#"
            if Seg.C in DIGIT[n]:
                display_lines[2] = "###"
            if Seg.SW in DIGIT[n]:
                display_lines[3] = "#" + display_lines[3][1:]
            if Seg.SE in DIGIT[n]:
                display_lines[3] = display_lines[3][:2] + "#"
            if Seg.S in DIGIT[n]:
                display_lines[4] = "###"

            # Add some extra characters for '0', '1', '4', and '7' to display correctly
            if (n == 0):
                display_lines[2] = "# #"
            elif (n == 1):
                display_lines[0] = display_lines[0][:2] + "#"
                display_lines[2] = display_lines[2][:2] + "#"
                display_lines[4] = display_lines[4][:2] + "#"
            elif (n == 4):
                display_lines[0] = "# #"
                display_lines[4] = display_lines[4][:2] + "#"
            elif (n == 7):
                display_lines[2] = display_lines[2][:2] + "#"
                display_lines[4] = display_lines[4][:2] + "#"


            for i in range(5):
                formatted_numbers_full[i] += (display_lines[i] + " ")

            formatted_numbers_separated.append('\n'.join(display_lines))

        formatted_number = '\n'.join(formatted_numbers_full)

        self.formatted_numbers_separated = formatted_numbers_separated
        self.formatted_number = formatted_number
        return formatted_number


if __name__ == '__main__':

    with open('day08_input.txt', 'r') as f:
        signals = f.readlines()


    count = 0
    sum = 0
    printout = ""

    for signal_line in signals:
        tests = signal_line.split()[:10]
        outputs = signal_line.split()[11:]

        # Generate an object to parse the numbers for this line
        disp = Display(tests, outputs)

        # Collect a printout of all numbers
        printout += disp.formatOutputNumbers() + "\n\n"


        ## Part 1
        for n in disp.getOutputNumbers():
            if n in [1, 4, 7, 8]:
                count += 1


        ## Part 2
        numstr = ''
        for n in disp.getOutputNumbers():
            numstr += str(n)
        sum += int(numstr)


    with open('day08_output.txt', 'w') as f:
        f.write(printout)

    print(f"[Part 1] There are {count} occurrences of the digits '1', '4', '7', or '8'.")

    print(f"[Part 2] The sum of all output numbers is {sum}.")
