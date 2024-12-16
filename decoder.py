import sys
import ast
import csv

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
    mode = data[2][:3]
    if mode == 'min':
        mode = 'm'
    elif mode == 'maj':
        mode = ''
    
    key += mode
    abc_output.append(f"K: {key}")

    return abc_output



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
        
        f_out.write(output)

if __name__ == "__main__":
    main()