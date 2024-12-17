import sklearn.neural_network as nn
import pandas
import random
import pickle


def makeMPL(training_X, training_y, possibleTokens):
    MLP = nn.MLPClassifier(hidden_layer_sizes=(64, 16), random_state=1, max_iter=500)
    MPLFit = MLP.fit(training_X, training_y)
    return MPLFit

def getData(data):
    #data = pandas.read_csv(filePath)
    training_X, training_y, testing_X, testing_y  = split_data(data, .8, 0)
    return training_X, training_y, testing_X, testing_y 

def split_data(data_set, train_percentage, seed):
    #shuffle data_set into a random order, using the passed in seed
    shuffled = data_set.sample(frac=1, random_state=seed)
    total_rows = shuffled.shape[0]
    
    # split the shuffled data into two new pandas DataFrame objects -- a training set and a testing set
    training_rows = int(round(train_percentage * total_rows))
    training = shuffled.iloc[:training_rows, :]
    testing = shuffled.iloc[training_rows:, :]

    # separate the attribute values and labels from both the training and testing sets
    #print("testing colums are", training.columns)
    training_X = training.drop("label", axis=1)
    training_y = training["label"]
   
    # split the testing attributes and labels
    testing_X = testing.drop("label", axis=1)
    testing_y = testing["label"]
    return training_X, training_y, testing_X, testing_y    

def convertCSVtoLongCSV(filePath, numColums=100):
    # data = open(filePath).read()
    # splitData = data.split("\n")
    df = pandas.DataFrame(columns=["label", "1.1", "1.2", "1.3","2.1", "2.2", "2.3","3.1", "3.2", "3.3","4.1", "4.2", "4.3","5.1", "5.2", "5.3"])
    # numAdded = 0
    # dataIndex = 0
    data = open("./swedish_tunes.csv").read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
    random.seed(0)
    random.shuffle(data)
    TrainDataStart = numColums

    for i in range(len(data)):
        data[i] = data[i][3:]
        for tokenIndex in range(len(data[i])):
            data[i][tokenIndex] = data[i][tokenIndex][2:len(data[i][tokenIndex])-1]
            data[i][tokenIndex] = data[i][tokenIndex].split(" ")
            data[i][tokenIndex] = toupleAafy(data[i][tokenIndex])
        if i<TrainDataStart:
            if len(data[i])>5:
                for j in range(5, len(data[i])):
                    addMap = []
                    try:
                        addMap.append(int(data[i][j-5][0]))
                    except:
                        addMap.append(0)
                    for sub in range(5):
                        for index in range(3):
                            try:
                                addMap.append(int(data[i][j-sub][index]))
                            except:
                                addMap.append(0)
                    # data[i][j-5][0], data[i][j-4][0], data[i][j-4][1], data[i][j-4][2], data[i][j-3][0], data[i][j-3][2], data[i][j-3][2], data[i][j-2][0], data[i][j-2][1], data[i][j-2][2], data[i][j-1][0],data[i][j-1][1],data[i][j-1][2], data[i][j-0][0],data[i][j-0][1],data[i][j-0][2]
                    # addMap = [data[i][j-5][0], data[i][j-4][0], data[i][j-4][1], data[i][j-4][2], data[i][j-3][0], data[i][j-3][2], data[i][j-3][2], data[i][j-2][0], data[i][j-2][1], data[i][j-2][2], data[i][j-1][0],data[i][j-1][1],data[i][j-1][2], data[i][j-0][0],data[i][j-0][1],data[i][j-0][2]]
                    df.loc[len(df)] = addMap
    return df

    # while numAdded<5000 and dataIndex<len(splitData):
    #     lineSplit = splitData[dataIndex].split(",")
    #     df = pd.concat([pd.DataFrame([[1,2]], columns=df.columns), df], ignore_index=True)

    # maxLen = 0
    # for line in splitData:
    #     if len(line)>maxLen:
    #         maxLen = len(line)
    # firstLine = ""
    # for i in range(maxLen):
    #     if i<maxLen-1:
    #         firstLine = firstLine + str(i) + ","
    #     else:
    #         firstLine = firstLine + str(i) + "\n"
    # data = firstLine + data
    # for i in range(len(splitData)):
    #     for j in range(len(splitData[i])+1, maxLen):
    #         splitData[i].append("0,")

def toupleAafy(changeList):
    """
    turns list into tuple recursivly
    """
    for i in range(len(changeList)):
        if isinstance(changeList[i], list):
            changeList[i] = toupleAafy(changeList[i])
    return tuple(changeList)


if __name__ == "__main__":
    print("hi world")
    df = convertCSVtoLongCSV("swedish_tunes.csv")
    #print("colums are ", df.columns)
    training_X, training_y, testing_X, testing_y  = getData(df)
    MLP = makeMPL(training_X, training_y, None)
    result = MLP.score(testing_X, testing_y)
    with open("MLPC.pickle", 'wb') as file:
        pickle.dump(MLP, file)

    print("score is", result)
    