import argparse

parser = argparse.ArgumentParser()
parser.add_argument('token_csv', type=argparse.FileType('r', encoding='latin-1'), help="Path to token csv file")
parser.add_argument('translation_file', type=argparse.FileType('w+'), help="Path to translation file")
parser.add_argument('output_file', type=argparse.FileType('w'), help="Path to output file")

args = parser.parse_args()

output_file = args.output_file

translation = []
translation_file = args.translation_file.readlines()
for line in translation_file:
    translation.append(line)

token_csv = args.token_csv.readlines()
for line in token_csv:
    line_tokens = line.split(',')
    for token in line_tokens:
        token = token.strip()
        try:
            translated_int = translation.index(token)
        except ValueError:
            translation.append(token)
            translated_int = len(translation) - 1
        # Write int, to new file
        output_file.write(str(translated_int) + ', ')
    output_file.write('\n')

# Dump new translation file to same pathname
translation_file = args.translation_file
translation_file.truncate(0)
translation_file.seek(0)
for item in translation:
    translation_file.write(item + '\n')

translation_file.close()
output_file.close()
args.token_csv.close()