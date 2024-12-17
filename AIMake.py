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
        self.states = {}
    def train(self, data):
        """
        data must be in the form of a list or touple of lists of 
        touples that contain a token and what token followed it
        """
        for datum in data:
            datamSeen = self.states.get(datum[0])
            if datamSeen == None:
                #print("adding", datum)
                self.states[datum[0]] = markovState(datum[0], seed=(self.rng.random())*10000)
            self.states[datum[0]].encounterToken(datum[1])
    def gen(self, token):
        """
        given token, give the next element of the song
        """
        tokenState = self.states.get(token)
        if tokenState != None:
            #print("bug did not happen")
            return self.states[token].goToNextToken()
        else:
            # print("note, feture not in data, if this happenes often it may be a bug")
            # print("token is", token)
            #print("possibleTokens are", self.states)
            #sys.exit()
            # for possibleStates in self.states:
                # print("all states are")
                # print(possibleStates, type(possibleStates))
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
    TrainDataStart = int(len(data)*.8)

    for i in range(len(data)):
        data[i] = data[i][3:]
        for tokenIndex in range(len(data[i])):
            data[i][tokenIndex] = data[i][tokenIndex][2:len(data[i][tokenIndex])-1]
            data[i][tokenIndex] = data[i][tokenIndex].split(" ")
            data[i][tokenIndex] = toupleAafy(data[i][tokenIndex])
        if i<TrainDataStart:
            toTrain = []
            for tokenIndex in range(len(data[i])-1):
                if data[i][tokenIndex+1] != "":
                    toTrain.append((data[i][tokenIndex], data[i][tokenIndex+1]))
            MarkModle.train(toTrain)

    testIngAccuracy(MarkModle, data[TrainDataStart:])
    #print("size is", len(MarkModle.states))
    

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
            # print("perdiction is", perdiction)
            # print("nextToken is", currLine[test+1])
            if perdiction == currLine[test+1]:
                #print("found Equal")
                numTestsPassed = numTestsPassed + 1
            numTests = numTests + 1
    print("out of ", numTests, numTestsPassed, "passed")
    print("this test accuracy is ", numTestsPassed/numTests)

def MarkovGen(startToken, length=None):
    """
    pass this a starting token and optionaly a lenght
    startToken= the token that will start the chain, either as a list or as a touple(not as a string)
    lenght the length of the result as an int(including inital token), if not specifyed or None will keep going until an end token is genorated
    returns the a list of tokens. Each token is in TOUPLE form.
    uese the pickeled markov modle.
    """
    if isinstance(startToken, list):
        startToken = toupleAafy(startToken)
    with open('markovTest.pickle', 'rb') as file:
        markovModle = pickle.load(file)
    if length == None:
        genList = [startToken]
        while genList[-1] != (":||", "0", "0"):
            nextGen = markovModle.gen(genList[-1])
            genList.append(nextGen)
    else:
        genList = [startToken]
        for i in range(1, length):
            nextGen = markovModle.gen(genList[-1])
            genList.append(nextGen)
    return genList





if __name__ == "__main__":
    print("hellow world")
    #genSaveMarkov()
    genList = MarkovGen((5, 2, 0), 20)
    print(genList)




