import sys
import os
import re

# TODO: HANDLE NATURALS

# start of each line in csv: t,m,s,[x,d,o],[x,d,o] etc.
# t = time signature
# m = mode
# s = song type


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
    "B": 11,
    "Cb": 11
}


def parse_abc(path):

    print('CURRENT PATH: ' + path)

    fileobj = open(path, 'r', encoding='utf-8')
    file = fileobj.readlines()
    fileobj.close()

    time_signature = ''
    mode = ''
    song_type = ''
    genre = ''
    dotted_adjustment = 0

    key = '' # for transposition purposes

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

    read_notes = False
    read_key = False
    read_default_note_duration = False

    for line in file:

        if '"@-20,30 Stämn."' in line:
            break

        # song type
        if line.startswith('R:'):
            line = line.replace(' ', '')
            song_type = line[2:].strip()
        # time signature
        elif line.startswith('M:'):
            line = line.replace(' ', '')
            time_signature = line[2:].strip()
        # default note duration
        elif line.startswith('L:'):
            read_default_note_duration = True
        # key and mode
        elif line.startswith('K:') and read_key == False:

            read_key = True

            line = line.replace(' ', '')
            line = line.lower()

            key = line[2].upper()

            print('Line length: ' + str(len(line)))

            if len(line) > 3:
                if line[3] == '#':
                    key += '#'
                elif line[3] == 'b':
                    key += 'b'
            else:
                key = 'C'

            if key == 'N':
                key = 'C'

            print('KEY: ' + key)

            
            if 'min' in line or 'm' in line:
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
                mode = 'major'

        # Stop reading if we encounter other types of lines after reading the first tune
        elif line.startswith('V:') and read_notes == True:
            break

        elif len(line) > 1 and (line[1] != ':' or line.startswith('|:')) and (len(line) != 0 and "utf-8" not in line) and not (line.startswith('V:2') or line.startswith('%')) and read_key and read_default_note_duration:
            line = line.replace(' ', '')
            line = re.sub(r'"[^"]*"', '', line)
            line = re.sub(r'![^!]*!', '', line)
            print(line)
            adjustment = 0
            i = 0
            while i < len(line):

                note = 0
                duration = 0
                octave = 0
                
                handled_tuplet = False

                c = line[i]

                if c == ' ':
                    i += 1

                # skip ornaments enclosed in {}
                elif c == '{':
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
                        if line[i+1] == '^':
                            adjustment += 1
                    elif c == "_":
                        adjustment -= 1
                        if line[i+1] == '_':
                            adjustment -= 1
                    elif c == '=':
                        adjustment = 0

                # tuplets
                elif c.isnumeric():
                    
                    # print('TUPLET')
                    # print(line[i])
                    # print(c)

                    handled_tuplet = True

                    tuplet = int(c)
                    duration = 1/tuplet
                    i += 1
                    tuplet_count = 0

                    while tuplet_count < tuplet and i < len(line):

                        # print (line[i])

                        if line[i] in "^_=":
                            if line[i] == "^":
                                adjustment += 1
                                if line[i+1] == '^':
                                    adjustment += 1
                            elif line[i] == "_":
                                adjustment -= 1
                                if line[i+1] == '_':
                                    adjustment -= 1
                            elif line[i] == '=':
                                adjustment = 0

                        
                        elif line[i].isalpha() and line[i].upper() in note_mapping:
                            note = note_mapping[line[i].upper()]
                            diatonic_degree = note_diatonic_mapping[note]

                            note = (
                                note
                                + key_adjustments[key][diatonic_degree] % 12
                            )

                            note = (note - key_mapping[key])

                            if note < 0:
                                octave -= 1

                            note = note % 12

                            note = (
                                note
                                + mode_adjustments[mode][diatonic_degree] 
                                + adjustment % 12
                            )
                            
                            adjustment = 0
                            
                            if c.isupper():
                                octave = -1

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

                            if dotted_adjustment != 0:
                                duration *= dotted_adjustment
                                dotted_adjustment = 0
                            
                            temp_adjustment = 0
                            temp_count = 0
                            
                            while i + 1 < len(line) and line[i+1] == '>':
                                temp_count += 1
                                temp_adjustment += (1/(2**temp_count))
                                i += 1
                        
                            temp_adjustment += 1
                            duration *= temp_adjustment
                            dotted_adjustment = 1 - (temp_adjustment - 1)

                            tuplet_count += 1
                        
                        i += 1
                        notes.append([note, duration, octave])


                # notes
                elif c.isalpha() and c.upper() in note_mapping:
                    # print(adjustment)
                    note = note_mapping[c.upper()]

                    diatonic_degree = note_diatonic_mapping[note]

                    note = (
                        note
                        + key_adjustments[key][diatonic_degree] % 12
                    )

                    note = (note - key_mapping[key])

                    if note < 0:
                        octave -= 1

                    note = note % 12

                    note = (
                        note
                        + mode_adjustments[mode][diatonic_degree] 
                        + adjustment % 12
                    )
                    
                    adjustment = 0
                    duration = 1
                    
                    if c.isupper():
                        octave = -1

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

                    if dotted_adjustment != 0:
                         duration *= dotted_adjustment
                         dotted_adjustment = 0
                    
                    temp_adjustment = 0
                    temp_count = 0
                    
                    while i + 1 < len(line) and line[i+1] == '>':
                        temp_count += 1
                        temp_adjustment += (1/(2**temp_count))
                        i += 1
                
                    temp_adjustment += 1
                    duration *= temp_adjustment
                    dotted_adjustment = 1 - (temp_adjustment - 1)

                # chords
                elif c == "[":
                    chord_notes = []
                    
                    i += 1 
                    
                    # read until closing bracket
                    while i < len(line) and line[i] != "]":

                        duration = 1

                        if line[i] in "^_=":
                            if line[i] == "^":
                                adjustment += 1
                                if line[i+1] == '^':
                                    adjustment += 1
                            elif line[i] == "_":
                                adjustment -= 1
                                if line[i+1] == '_':
                                    adjustment -= 1
                            elif line[i] == '=':
                                adjustment = 0

                        # note
                        if line[i].isalpha() and line[i].upper() in note_mapping:
                            note = note_mapping[line[i].upper()]
                            diatonic_degree = note_diatonic_mapping[note]

                            note = (
                                note
                                + key_adjustments[key][diatonic_degree] % 12
                            )

                            note = (note - key_mapping[key])

                            if note < 0:
                                octave -= 1

                            note = note % 12

                            note = (
                                note
                                + mode_adjustments[mode][diatonic_degree] 
                                + adjustment % 12
                            )

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

                            if dotted_adjustment != 0:
                                duration *= dotted_adjustment
                                dotted_adjustment = 0
                            
                            temp_adjustment = 0
                            temp_count = 0
                            
                            while i + 1 < len(line) and line[i+1] == '>':
                                temp_count += 1
                                temp_adjustment += (1/(2**temp_count))
                                i += 1
                        
                            temp_adjustment += 1
                            duration *= temp_adjustment
                            dotted_adjustment = 1 - (temp_adjustment - 1)

                            chord_notes.append([note, duration, octave])

                        i += 1

                    note = chord_notes
                    octave = 0
                
                # add encoded note
                if (not (note == 0 and duration == 0 and octave == 0)) and handled_tuplet == False :
                    notes.append([note, duration, octave])
                    read_notes = True
                i += 1
                
    if notes != []: 
        if notes[-1][0] != '||':
            if notes[-1][0] == ':|':
                notes[-1][0] = ':||'
            else:
                notes[-1][0] = '||'

    encoding = [time_signature, mode, song_type]
    for note in notes:
        encoding.append(note)

    return encoding



# run the encoder on a given file
def process_file(file_path):
    # try:
        encoding = parse_abc(file_path)
        print(f"Processed file: {file_path}")
        print(encoding)
        return encoding 
    # except Exception as e:
    #     print(f"Error processing file {file_path}: {e}")


def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    
    # root directory to scan for .abc files
    output_path = sys.argv[1]
    root_directory = sys.argv[2]
    with open(output_path, 'w') as f_out:
        # make sure directory is valid
        if not os.path.isdir(root_directory):
            # print(f"Error: {root_directory} is not a valid directory.")
            # sys.exit(1)
            process_file(root_directory) # single file
        else:
        # go through all subdirectories
            for subdir, _, files in os.walk(root_directory):
                for file in files:
                    if file.endswith('.abc'):
                        # queue each .abc file
                        file_path = os.path.join(subdir, file)
                        encoded_list = process_file(file_path)
                        if encoded_list != ['','','']:
                            for element in encoded_list:
                                if element != '':
                                    element_without_commas = str(element).replace(",", '')
                                    f_out.write(str(element_without_commas) + ', ')
                            f_out.write('\n')

if __name__ == "__main__":
    main()
