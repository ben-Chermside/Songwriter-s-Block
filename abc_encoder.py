import sys
import os

# start of each line in csv: t,m,s,g,[],[],[]
# t = time signature
# m = mode
# s = song type
# g = genre


# format for each note: [x,d,o]
# x = letter note
# d = (relative) duration
# o = octave


def parse_abc(path):
    file = open(path, 'r')
    file = file.readlines()

    time_signature = ''
    mode = ''
    song_type = ''
    genre = ''

    key = '' # for transposition purposes

    notes = []

    for line in file:
        # song type
        if line.startswith('R:'):
            line = line.replace(' ', '')
            song_type = line[2:]
        # time signature
        if line.startswith('M:'):
            line = line.replace(' ', '')
            time_signature = line[2:]
        # key and mode
        if line.startswith('K:'):
            line = line.replace(' ', '')
            line = line.lower()

            key = line[3]

            if len(line[2:]) == 1:
                mode = 'major'
            elif line[2:] == 'min' or line[2:] == 'm':
                mode = 'minor'
            elif line[2:] == 'dor':
                mode = 'dorian'
            elif line[2:] == 'phr':
                mode = 'phrygian'
            elif line[2:] == 'lyd':
                mode = 'lydian'
            elif line[2:] == 'mix':
                mode = 'mixolydian'
            elif line[2:] == 'loc':
                mode = 'loc'
            else:
                mode = 'unspecified'

        note = ''
        duration = ''
        octave = 0

        if (line[2] != ':' or line.startswith('|:')) and (len(line) != 0 and not line.endswith("utf-8")):
            i = 0
            while i < len(line):
                c = line[i]

                if c == ' ':
                    i += 1
                    continue
                    
                if c.isalpha():
                    note += c
                    if c.islower():
                        octave += 1
                    elif c.isupper():
                        octave -= 1
                

                # add encoded note
                notes.append([note, duration, octave])

                i += 1
            return {
                "time_signature": time_signature,
                "mode": mode,
                "song_type": song_type,
                "key": key,
                "notes": notes
            }


def main():
    path = sys.argv[1]
    print(parse_abc(path))


if __name__ == "__main__":
    main()



                

            









