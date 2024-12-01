#This contains a function that extracts an ABC file and returns an object with all the info

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
