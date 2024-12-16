import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input_file', type=argparse.FileType('r', encoding='latin-1'), help="Path to token csv file")
parser.add_argument('translation_file', type=argparse.FileType('w+'), help="Path to translation file")
parser.add_argument('output_file', type=argparse.FileType('w'), help="Path to output file")
parser.add_argument('-r', '--reverse', action='store_true')

args = parser.parse_args()

output_file = args.output_file

translation = []
translation_file = args.translation_file.readlines()
for line in translation_file:
    translation.append(line)

input_file = args.input_file.readlines()

for line in input_file:
    line_tokens = line.split(',')
    for token in line_tokens:
        token = token.strip()
        if args.reverse:
            # This will throw an uncaught IndexError if an integer does not exist in the translation
            translated = translation[token]
        else:
            try:
                translated = translation.index(token)
            except ValueError:
                translation.append(token)
                translated = len(translation) - 1
        # Write int, to new file
        output_file.write(str(translated) + ', ')
    output_file.write('\n')

# Dump new translation file to same pathname
translation_file = args.translation_file
translation_file.truncate(0)
translation_file.seek(0)
for item in translation:
    translation_file.write(item + '\n')


translation_file.close()
output_file.close()
args.input_file.close()