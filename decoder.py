import sys
import ast
import csv
import re

dotted = False
tuplet = 0
tuplet_counter = 0

def parse_token(item):

    global dotted
    global tuplet 
    global tuplet_counter 

    note = ''

    # Process the notes and bars
    note_map_lower = {0: "C", 1: "^C", 2: "D", 3: "_E", 4: "E", 5: "F", 6: "^F",
                7: "G", 8: "^G", 9: "A", 10: "_B", 11: "B", -1: "z"}
    note_map_upper = {0: "c", 1: "^c", 2: "d", 3: "_e", 4: "e", 5: "f", 6: "^f",
                7: "g", 8: "^g", 9: "a", 10: "_b", 11: "b", -1: "z"}

    if not isinstance(item, list):
        formatted_string = item.replace(' ', ',')
        formatted_string = formatted_string.replace("'", '"')

        if formatted_string != '':
            item = ast.literal_eval(formatted_string)
    if item != '':
        if isinstance(item[0], list):
            return '[' + parse_token(item[0]) + ']'
        elif isinstance(item[0], str):
            return item[0]
        else:
            # print('HEY')
            # print(item[0])
            # note name and octave
            if item[2] <= -1:
                note += note_map_lower[item[0] % 12]
            else:
                note += note_map_upper[item[0] % 12]

            # extra octaves
            if item[2] < -1:
                for i in range(0, abs(item[2])):
                    note += ","
            elif item[2] > 0:
                for i in range(0, item[2]):
                    note += "'"
            
            # duration
            if dotted == False and tuplet_counter == tuplet:
                # check for tuplets
                # TODO: Handle 0.6666666666 and stuff like that
                if item[1] == (1/3):
                    tuplet = 3
                    note = '(3' + note
                    tuplet_counter += 1
                elif item[1] == (1/6):
                    tuplet = 6
                    note = '(6' + note
                    tuplet_counter += 1
                elif item[1] == (1/9):
                    tuplet = 9
                    note = '(9' + note
                    tuplet_counter += 1
                # check for dotted rhythms
                elif item[1] == 1.5:
                    note += '>'
                    dotted = True
                elif item[1] == 1.75:
                    note += '>>'
                    dotted = True
                elif item[1] == 3.5:
                    note += '2>>'
                    dotted = True
                elif item[1] == 0.75:
                    note += '/>'
                    dotted = True
                else:   
                    if item[1] < 1:
                        if item[1] == 0.5:
                            note += '/'
                        elif item[1] == 0.25:
                            note += '//'
                        elif item[1] == 0.125:
                            note += '///'
                        else: 
                            note += str(item[1])
                    else:
                        note += str(item[1])
            else:
                if tuplet_counter != tuplet:
                    tuplet_counter += 1
                    if tuplet == tuplet_counter:
                        tuplet_counter = 0
                        tuplet = 0
                else:
                    dotted = False

            # print(item_list)

    return note

def decode(data):

    abc_output = []

    # song type
    abc_output.append(f"R: {data[2]}")

    # time signature
    abc_output.append(f"M: {data[0]}")

    # default note duration
    abc_output.append("L: 1/8") 

    # key and mode
    key = 'C'
    mode = data[1][:3]
    if mode == 'min':
        mode = 'm'
    elif mode == 'maj':
        mode = ''
    
    key += mode
    abc_output.append(f"K: {key}")

    string_of_notes = ''

    data = data[3:]
    print(data)

    for item in data:
        if item != "''":
            string_of_notes += parse_token(item)

    abc_output.append(string_of_notes)

    return abc_output

def add_newlines_after_bars(abc_text):
    def replacer(match):
        # match groups: group 1 captures up to the 4th '|', group 2 captures the rest
        bar_section, rest = match.groups()
        return f"{bar_section}\n{rest}"

    return re.sub(r"((?:.*?\|){4})([^|\d])", replacer, abc_text)


def data_to_list(file_path):
    data = []
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:

            line = line.replace("'", '"')

            # Parse the CSV data
            reader = csv.reader([line], skipinitialspace=True)
            for row in reader:
                structured_data = []
                for item in row:
                    try:
                        # Try to evaluate items as Python objects (e.g., lists, numbers)
                        structured_data.append(ast.literal_eval(item))
                    except (SyntaxError, ValueError):
                        # If it fails, keep the item as a string
                        structured_data.append(item)
                    # print(item)
            
            data.append(structured_data)
        return data
    

def main():
    if len(sys.argv) != 3:
        sys.exit(1)
    
    output = ''

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    data_list = data_to_list(input_path)

    for list in data_list:
        output += str(decode(list)) + '\n'
    

    with open(output_path, 'w') as f_out:
        output = output.replace("]", '')
        output = output.replace("[", '')
        output = output.replace("'", '')
        output = output.replace(",", '\n')

        output = add_newlines_after_bars(output)

        f_out.write(output)

if __name__ == "__main__":
    main()