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

    key = 0 # for transposition purposes

    notes = []

    note_mapping = {
        "C": 0,
        "D": 2,
        "E": 4,
        "F": 5,
        "G": 7,
        "A": 9,
        "B": 11,
        "H": 11,
        }

    for line in file:
        print(line)
        # song type
        if line.startswith('R:'):
            line = line.replace(' ', '')
            song_type = line[2:]
        # time signature
        elif line.startswith('M:'):
            line = line.replace(' ', '')
            time_signature = line[2:]
        # key and mode
        elif line.startswith('K:'):
            line = line.replace(' ', '')
            line = line.lower()

            key = note_mapping[line[3].upper()]

            if line[4] == '#':
                key = (key + 1) % 12
            if line[4] == 'b':
                key = (key - 1) % 12

            if 1 <= len(line[2:]) <= 2:
                mode = 'major'
            elif 'min' in line or 'm' in line:
                mode = 'minor'
            elif 'dor' in line:
                mode = 'dorian'
            elif 'phr' in line:
                mode = 'phrygian'
            elif 'lyd' in line:
                mode = 'lydian'
            elif 'mix' in line:
                mode = 'mixolydian'
            elif 'loc' in line:
                mode = 'loc'
            else:
                mode = 'unspecified'
        elif len(line) > 1 and  (line[1] != ':' or line.startswith('|:')) and (len(line) != 0 and "utf-8" not in line):
            adjustment = 0

            i = 0
            while i < len(line):

                note = 0
                duration = 0
                octave = 0

                c = line[i]

                if c == ' ':
                    i += 1
                    
                # barlines and repeats
                elif c in '|:':
                    if i + 1 < len(line) and line[i + 1] in ':|':
                        # repeats
                        symbol = c + line[i + 1]
                        notes.append([symbol, 0, 0])  
                        i += 1  
                    else:
                        # single bar line
                        notes.append([c, 0, 0])
                
                # accidentals
                elif c in "^_=":
                    if c == "^":
                        adjustment += 1
                    elif c == "_":
                        adjustment -= 1
                    elif c == '=':
                        adjustment = 0
                    i += 1

                # notes
                elif c.isalpha() and c.upper() in note_mapping:
                    note = (note_mapping[c.upper()] + adjustment) % 12                    
                    duration = 1
                    
                    if c.isupper():
                        octave = -1
                    else:
                        octave = 0

                    # extra octave adjustments
                    while i + 1 < len(line) and line[i + 1] in ["'", ","]:
                        if line[i + 1] == "'":
                            octave += 1
                        elif line[i + 1] == ",":
                            octave -= 1
                        i += 1
                    
                    # duration
                    while i + 1 < len(line) and (line[i + 1].isdigit() or line[i + 1] == "/"):
                        i += 1
                        if line[i] == "/":
                            duration /= 2 
                        elif line[i].isdigit():
                            duration *= int(line[i])

                # add encoded note
                notes.append([note, duration, octave])
                adjustment
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



                

            









