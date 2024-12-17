import torch.nn
import random
import pandas
import random
import pickle
from abc_encoder import parse_abc
import os
import sys

# class modle:
#     def __init__(self, possableTokens, seed=None, tokenSize=6):
#         if seed != None:
#             random.seed(seed)
#             self.tokenMap = {}
#             for token in possableTokens:
#                 self.tokenMap[token] = []
#                 for i in range(tokenSize):
#                     self.tokenMap[token].append(random.uniform(0, 1))
            
#notes, defult size of d_modle is 512, I will try a lower number cause there are less possible tokens here so it 
# seemed like the modle would need less data per token. It could be intresting to see what a higher value would change.
#



def makeTrainingSet(data, trainPrecentage=.8):
    pass
    # data = open("./swedish_tunes.csv").read()
    # data = data.split("\n")
    # dataSize = len(data)
    # trainSize = int(dataSize*trainPrecentage)
    # dataSets = []
    # for line in range(trainSize):
    #     currLine = data[line]
    #     splitList = currLine.split(",")
    #     currDataSet = []
    #     currDataSet.append(splitList[0])
    #     currDataSet.append(splitList[1])
    #     currDataSet.append(splitList[2])
    #     currDataSet.append([])
    #     for currElem in range(3, len(splitList)):
    #         pass
        
    #     #currDataSet[3]


    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            worked = False
            try:
                testEncoding = parse_abc(filepath)
                worked = True
            except KeyError: #I encountered an error on some of the parcings, this may change if parce_abc() is updated
                print("encountered key error")
            except Exception:
                print("unspecifyed exception on file", filepath)
            if worked:
                pass
        




def trainModleTransformer(data, numEpocs=1000, lernRate=0.001):
    """
    trains a transformer model on the data, 
    returns the model
    """

    trainX, trainY = makeTrainingSet(data)

    modle = torch.nn.Transformer(d_modle=256)
    crLoss = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(modle.parameters(), lr=lernRate)

    for epoc in range(numEpocs):
        train_predictions = network(train_X)
        train_loss = crLoss(train_predictions, train_y)
        optimizer.zero_grad()
        train_loss.backward()
        optimizer.step()


    return modle

class markovState:
    """
    a helper class for markov
    """
    def __init__(self, token, seed=0):
        """
        creates a new marcove chain with no data,
        if selected, seed is used to choose what token to choose from the possible setss
        """
        self.seen = 0
        self.token = token
        self.encounteredTokens = {}
        self.seed = seed
        self.rng = random.Random(int(self.seed))
    def encounterToken(self, token):
        """
        used to train the markovState to indicate that the next example has 
        token before this self.token in training data
        """
        self.seen = self.seen + 1
        if self.encounteredTokens.get(token) != None:
            self.encounteredTokens[token] = self.encounteredTokens[token] + 1
        else:
            self.encounteredTokens[token] = 1
    def goToNextToken(self):
        selection = int(self.rng.random()*self.seen)
        for token in self.encounteredTokens:
            selection = selection - self.encounteredTokens[token]
            if selection<1:
                return token
        print("markov chain error, self.seen appears to be diff form sum of self.encountered tokens")
        return None





class markov:
    """
    This is a markov modle, it will suck, but dont let that discurage you (:
    """
    def __init__(self, seed=0):
        self.seed = seed
        self.rng = random.Random(self.seed)
    def train(self, data):
        """
        data must be in the form of a list or touple of lists of 
        touples that contain a token and what token followed it
        """
        self.states = {}
        for datum in data:
            datamSeen = self.states.get(datum[0])
            if datamSeen == None:
                self.states[datum[0]] = markovState(datum[0], seed=(self.rng.random())*10000)
            self.states[datum[0]].encounterToken(datum[1])
    def gen(self, token):
        """
        given token, give the next element of the song
        """
        tokenState = self.states.get(token)
        if tokenState != None:
            return self.states[token].goToNextToken()
        else:
            print("note, feture not in data, if this happenes often it may be a bug")
            print("token is", token)
            #print("possibleTokens are", self.states)
            #sys.exit()
            for possibleState in self.states:
                return self.states[possibleState].goToNextToken()


#Here I will put the code to actualy genorate and train a markov modle

def genSaveMarkov():
    MarkModle = markov()
    
    data = open("./swedish_tunes.csv").read()
    data = data.split("\n")
    for i in range(len(data)):
        data[i] = data[i].split(",")
    random.seed(0)
    random.shuffle(data)
    takeIndex = int(len(data)*.8)
    for i in range(len(data)):
        currLine = data[i]
        data[i] = data[i][3:]
        for tokenIndex in range(len(currLine)):
            data[i][tokenIndex] = data[i][tokenIndex][2:len(data[i][tokenIndex])-1]
            data[i][tokenIndex] = data[i][tokenIndex].split(" ")
            data[i][tokenIndex] = toupleAafy(data[i][tokenIndex])
        if i<tokenIndex:
            toTrain = []
            for tokenIndex in range(len(currLine)-1):
                toTrain.append((currLine[tokenIndex], currLine[tokenIndex+1]))
            MarkModle.train(toTrain)
    
    testIngAccuracy(MarkModle, data[tokenIndex:])
    

    with open("markovTest.pickle", 'wb') as file:
        pickle.dump(MarkModle, file)

def toupleAafy(changeList):
    """
    turns list into tuple recursivly
    """
    for i in range(len(changeList)):
        if isinstance(changeList[i], list):
            changeList[i] = toupleAafy(changeList[i])
    return tuple(changeList)
            

def testIngAccuracy(modle, testData):
    numTests = 0
    numTestsPassed = 0
    for i in range(len(testData)):
        currLine = testData[i]
        for test in range(len(currLine)-1):
            perdiction = modle.gen(currLine[test])
            if perdiction == currLine[test+1]:
                numTestsPassed = numTestsPassed + 1
            numTests = numTests + 1
    print("out of ", numTests, numTestsPassed, "passed")
    print("this test accuracy is ", numTestsPassed/numTests)


if __name__ == "__main__":
    print("hellow world")
    genSaveMarkov()#abc is the name of the directory I have the abc files,




