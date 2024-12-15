import sys
import os

# TODO: HANDLE TRIPLETS!
# DEAL WITH DOTTED RHYTHMS
# FIX OCTAVES WHEN TRANSPOSING TO C

# start of each line in csv: t,m,s,g,[x,d,o],[x,d,o] etc.
# t = time signature
# m = mode
# s = song type
# g = genre


# format for each note: [x,d,o]
# x = letter note
# d = (relative) duration
# o = octave

key_adjustments = {
    "C":  [0, 0, 0, 0, 0, 0, 0],   
    "G":  [0, 0, 0, 0, 0, 0, 1],   
    "D":  [1, 0, 0, 1, 0, 0, 0],   
    "A":  [1, 0, 0, 1, 1, 0, 0],    
    "E":  [1, 1, 0, 1, 1, 0, 0],   
    "B":  [1, 1, 0, 1, 1, 1, 0],    
    "F#": [1, 1, 1, 1, 1, 1, 0],   
    "C#": [1, 1, 1, 1, 1, 1, 1],
    "F":  [0, 0, 0, 0, 0, 0, -1],   
    "Bb": [0, 0, -1, 0, 0, 0, -1],  
    "Eb": [0, 0, -1, 0, 0, -1, -1], 
    "Ab": [0, -1, -1, 0, 0, -1, -1],
    "Db": [0, -1, -1, 0, -1, -1, -1],
    "Gb": [-1, -1, -1, 0, -1, -1, -1], 
    "Cb": [-1, -1, -1, -1, -1, -1, -1], 
}

mode_adjustments = {
    "major": [0, 0, 0, 0, 0, 0, 0],
    "dorian": [0, 0, -1, 0, 0, 0, -1],
    "phrygian": [0, -1, -1, 0, 0, -1, -1],
    "lydian": [0, 0, 0, 1, 0, 0, 0],
    "mixolydian": [0, 0, 0, 0, 0, 0, -1],
    "minor": [0, 0, -1, 0, 0, -1, -1],
    "locrian": [0, -1, -1, 0, -1, -1, -1]
}

key_mapping = {
    "C": 0,
    "Db": 1,
    "D": 2,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "Ab": 8,
    "A": 9,
    "Bb": 10,
    "B": 11
}


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

    note_diatonic_mapping = {
        0: 0,
        2: 1,
        4: 2,
        5: 3,
        7: 4,
        9: 5,
        11: 6,
    }

    for line in file:
        print(line)
        # song type
        if line.startswith('R:'):
            line = line.replace(' ', '')
            song_type = line[2:].strip()
        # time signature
        elif line.startswith('M:'):
            line = line.replace(' ', '')
            time_signature = line[2:].strip()
        # key and mode
        elif line.startswith('K:'):
            line = line.replace(' ', '')
            line = line.lower()

            key = line[2].upper()

            if len(line) > 2 and line[3] == '#':
                key += '#'
            if len(line) > 2 and line[3] == 'b':
                key += 'b'

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
                mode = 'locrian'
            else:
                mode = 'unspecified'
        elif len(line) > 1 and (line[1] != ':' or line.startswith('|:')) and (len(line) != 0 and "utf-8" not in line) and ('|' in line):
            line = line.replace(' ', '')
            adjustment = 0

            i = 0
            while i < len(line):

                note = 0
                duration = 0
                octave = 0

                c = line[i]

                if c == ' ':
                    i += 1

                # skip extra stuff enclosed in quotes
                if c == '"':
                    i += 1
                    while i < len(line) and line[i] != '"':
                        i += 1
                    i += 1 

                # skip extra stuff enclosed in !
                if c == '!':
                    i += 1
                    while i < len(line) and line[i] != '!':
                        i += 1
                    i += 1 

                # skip ornaments enclosed in {}
                if c == '{':
                    i += 1
                    while i < len(line) and line[i] != '}':
                        i += 1
                    i += 1 
                    
                # barlines and repeats
                elif c == '|':
                    if i + 1 < len(line) and line[i + 1] == ':':  # |:
                        notes.append(['|:', 0, 0])  
                        i += 1 
                    elif i + 1 < len(line) and line[i + 1] == '1':  # |1 
                        notes.append(['|1', 0, 0])  
                        i += 1  
                    elif i + 1 < len(line) and line[i + 1] == '2':  # |2 
                        notes.append(['|2', 0, 0])  
                        i += 1  
                    elif i + 1 < len(line) and line[i + 1] == '|':  # || 
                        notes.append(['||', 0, 0])  
                        i += 1  
                    else:
                        notes.append(['|', 0, 0])  # |
                elif c == ':':
                    if i + 1 < len(line) and line[i + 1] == '|':  
                        if i + 2 < len(line) and line[i + 2] == '1':  # ":|1"
                            notes.append([':|1', 0, 0])  
                            i += 2
                        elif i + 2 < len(line) and line[i + 2] == '2':  # ":|2"
                            notes.append([':|2', 0, 0]) 
                            i += 2  
                        else:
                            notes.append([':|', 0, 0])  # :|
                            i += 1
                    elif i + 1 < len(line) and line[i + 1] == ':':
                        notes.append(['::', 0, 0])  # ::
                        i += 1
                
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
                    note = note_mapping[c.upper()]
                    note = (
                        note
                        + key_adjustments[key][note_diatonic_mapping[note]] % 12
                    )
                    note = (note - key_mapping[key]) % 12

                    note = (
                        note
                        + mode_adjustments[mode][note_diatonic_mapping[note]] 
                        + adjustment % 12
                    )
                    
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

                # chords
                elif c == "[":
                    chord_notes = []
                    
                    i += 1 
                    
                    # read until closing bracket
                    while i < len(line) and line[i] != "]":

                        duration = 1

                        # note
                        if line[i].isalpha() and line[i].upper() in note_mapping:
                            note = note_mapping[line[i].upper()]
                            note = (
                                note
                                + key_adjustments[key][note_diatonic_mapping[note]]
                                + mode_adjustments[mode][note_diatonic_mapping[note]] 
                                + adjustment
                            )   
                            note = note % 12
                            if line[i].isupper():
                                octave = -1
                            else:
                                octave = 0

                            # octave
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

                            chord_notes.append([note, duration, octave])

                        i += 1

                    note = chord_notes
                    octave = 0

                # add encoded note
                if not (note == 0 and duration == 0 and octave == 0):
                    notes.append([note, duration, octave])
                adjustment
                i += 1

    if notes[-1][0] != '||':
        if notes[-1][0] == ':|':
            notes[-1][0] = ':||'
        else:
            notes[-1][0] = '||'

    encoding = ['Swedish', song_type, time_signature, key, mode]
    for note in notes:
        encoding.append(note)

    return encoding


def main():
    path = sys.argv[1]
    print(parse_abc(path))


if __name__ == "__main__":
    main()
