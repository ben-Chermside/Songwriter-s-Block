#This contains a function that extracts an ABC file and returns an object with all the info
import sys

def abort(message):
    print(message)
    sys.exit(0)



#should do the same thing, I copied this off of another ABC file format project
#project here, https://github.com/xoliver/abctools/blob/master/abctools.py
#licence allows, https://github.com/xoliver/abctools/blob/master/LICENSE
#no idea if works better than my version, probaby does
def load_abc_file(fname):
    """
    Read ABC file and return a dictionary containing the different headers
    plus the tune in the key 'tune'
    """

    abc = {}
    with open(fname, 'r') as f:
        lines = f.readlines()
    i = 0
    for line in lines:
        line = line.strip()
        parts = line.split(':')
        header = parts[0].strip().upper()
        if len(header) != 1 or header not in ('X', 'T', 'R', 'M', 'L', 'K'):
            break
        abc[header] = ':'.join(parts[1:]).strip()
        i += 1

    abc['tune'] = ' '.join(map(lambda x: x.strip(), lines[i:])).strip()

    if 'X:' in abc['tune']:
        abort('Oops, more than one tune found in this file!')

    return abc





def extractFile(filePath):
    """
	take in a filePath and extracts the ABC file, if no file exists produces an error.
	return a dictionary with the elements of the ABC file.
	the keys will have the field 'music' that will have a string of the music.
	In addition, it will have an extra field for every additional field that was in the file, none of these are guaranteed to exist
	For example, if the file has a composer, that will be represented by the key "C" and value of the name, but if there is not than no C field will exist
    """
    feildNames = "ABCDEFGHIJKLMmNOPQRrSsTUVWwXZ" #feilds are makred with one of these characters followed by :
    #more info about feilds https://abcnotation.com/wiki/abc:standard:v2.1/#how_to_read_this_document
    try:
        file = open(filePath).read()#read file as string
    except FileExistsError:
        print("error, no such file at", filePath, "found." )
    info = {}
    splitData = file.split("\n")#split into each lines
    fileLine = 2
    while fileLine<len(splitData) and len(splitData[fileLine]) > 3 and splitData[fileLine][0] in feildNames and splitData[fileLine][1] == ":":#checks if we have gotten to music yet
        info[splitData[fileLine][0]] = splitData[fileLine][3:]#the first 3 chars are (in feildNames), ':', ' '
        fileLine = fileLine + 1
    rest = ""
    for i in range(fileLine, len(splitData)):
        rest = rest + splitData[i] + "\n"
    info['music'] = rest
    return info


if __name__ == "__main__":
    #for testing
    data = extractFile("C:\\Users\\bcher\\OneDrive\\Desktop\\oberlin\\7th-term\\mLearning\\songWrightersBlock\\Songwriter-s-Block\\abc\\_Bl_E5nnOlles_Hambo_70414f.abc")
    print("resulting data is", data)
