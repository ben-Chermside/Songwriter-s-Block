import torch.nn
import random
import pandas
import random
import pickle
from abc_encoder import parse_abc
import os

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



def makeTrainingSet(data):
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
    def __init__(self, token, seed=random.randint(0, 1000000)):
        """
        creates a new marcove chain with no data,
        if selected, seed is used to choose what token to choose from the possible setss
        """
        self.seen = 1
        self.token = token
        self.encounteredTokens = {}
        self.seed = seed
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
        selection = random.randint(1, self.seen)
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
    def __init__(self):
        pass
    def train(self, data):
        """
        data must be in the form of a list or touple of lists of 
        touples that contain a token and what token followed it
        """
        self.states = {}
        for datum in data:
            datamSeen = self.states.get(datum[0])
            if datamSeen == None:
                self.states[datum[0]] = markovState(datum[0])
            self.states[datum[0]].encounterToken(datum[1])
    def gen(self, token):
        """
        given token, give the next element of the song
        """
        return self.states[token].goToNextToken()


#Here I will put the code to actualy genorate and train a markov modle

def genSaveMarkov(directory):
    MarkModle = markov()
    #this code loops through all the files in the directory, that is where I have abc files,
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
                testEncoding = testEncoding[5:]
                for i in range(len(testEncoding)):
                    testEncoding[i] = toupleAafy(testEncoding[i])
                trainingData = []
                for i in range(len(testEncoding)-1):
                    trainingData.append([testEncoding[i], testEncoding[i+1]])
                MarkModle.train(trainingData)
    # with open("markovTest.pickle", 'wb') as file:
    #     pickle.dump(MarkModle, file)

def toupleAafy(changeList):
    """
    turns list into tuple recursivly
    """
    for i in range(len(changeList)):
        if isinstance(changeList[i], list):
            changeList[i] = toupleAafy(changeList[i])
    return tuple(changeList)
            


if __name__ == "__main__":
    print("hellow world")
    genSaveMarkov("abc")#abc is the name of the directory I have the abc files,



