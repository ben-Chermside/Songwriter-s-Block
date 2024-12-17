import torch.nn
import random
import pandas
import random
import pickle
from abc_encoder import parse_abc
import os
import sys
import math

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



def makeTrainingSet(datapath, trainPrecentage=.8):
    data = open(datapath).read()
    data = data.split("\n")
    maxLen = 0
    if data[-1] == "":
        data.pop()
    allInts = set()
    for i in range(len(data)):
        data[i] = data[i].split(",")
    for i in range(len(data)):
        lineLen = len(data[i])
        if lineLen > maxLen:
            maxLen = lineLen
        for j in range(lineLen):
            data[i][j] = int(data[i][j])
            allInts.add(data[i][j])
    allInts = list(allInts)
    allInts.sort()
    maxData = allInts[-1]#maxData will be expected to be 1177
    maxDataBig = maxData + 1
    for i in range(len(data)):#This adds the next int up to the start of each line so all songs are the same size
        lineStart = (maxLen*len(data[i]))*[maxDataBig]
        data[i] = lineStart + data[i]
    
    return data, maxDataBig



    
    



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


    # for filename in os.listdir(directory):
    #     filepath = os.path.join(directory, filename)
    #     if os.path.isfile(filepath):
    #         worked = False
    #         try:
    #             testEncoding = parse_abc(filepath)
    #             worked = True
    #         except KeyError: #I encountered an error on some of the parcings, this may change if parce_abc() is updated
    #             print("encountered key error")
    #         except Exception:
    #             print("unspecifyed exception on file", filepath)
    #         if worked:
    #             pass
        

def batchify(data, bsz):
    # Work out how cleanly we can divide the dataset into bsz parts.
    nbatch = data.size(0) // bsz
    # Trim off any extra elements that wouldn't cleanly fit (remainders).
    data = data.narrow(0, 0, nbatch * bsz)
    # Evenly divide the data across the bsz batches.
    data = data.view(bsz, -1).t().contiguous()
    return data#.to(device)


def repackage_hidden(h):
    """Wraps hidden states in new Tensors, to detach them from their history."""

    if isinstance(h, torch.Tensor):
        return h.detach()
    else:
        return tuple(repackage_hidden(v) for v in h)

def get_batch(source, i):
    seq_len = min(35, len(source) - 1 - i)
    data = source[i:i+seq_len]
    target = source[i+1:i+1+seq_len].view(-1)
    return data, target


def trainModleTransformer(dataPath, numEpocs=1000, lernRate=0.001):
    """
    trains a transformer model on the data, 
    returns the model
    """

    #trainX, trainY = makeTrainingSet(dataPath)

    data, maxToken = makeTrainingSet(dataPath, 0.8)
    lineLen = len(data[0])
    # numBatches = 50
    # batchSize = math.ceil(len(data)/numBatches)
    eval_batch_size = 10
    corpus = data.Corpus(data)

    train_data = batchify(corpus.train, 20)
    val_data = batchify(corpus.valid, eval_batch_size)
    test_data = batchify(corpus.test, eval_batch_size)

    embedding_dim = 256
    transformer = torch.nn.Transformer()
    model = model.TransformerModel(maxToken+1, 200, 2, 200, 2, 0.2)#.to(device)


    optimizer = torch.optim.Adam(transformer.parameters(), lr=lernRate)
    criterion = torch.nn.CrossEntropyLoss(ignore_index=maxToken)
    for i in range(numEpocs):
        for batchNum in range(numBatches):
            currBatch = []
            for batchInd in range(batchSize):
                currIndex = batchNum*batchSize+batchInd
                currBatch.append(data[currIndex])
            output = transformer(currBatch)
            loss = criterion(output)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    lr = lernRate


    model.train()
    total_loss = 0.
    ntokens = len(corpus.dictionary)
    for batch, i in enumerate(range(0, train_data.size(0) - 1, 35)):
        data, targets = get_batch(train_data, i)
        # Starting each batch, we detach the hidden state from how it was previously produced.
        # If we didn't, the model would try backpropagating all the way to start of the dataset.
        model.zero_grad()
        output = model(data)
        output = output.view(-1, ntokens)
        loss = criterion(output, targets)
        loss.backward()

        # `clip_grad_norm` helps prevent the exploding gradient problem in RNNs / LSTMs.
        torch.nn.utils.clip_grad_norm_(model.parameters(), .25)
        for p in model.parameters():
            p.data.add_(p.grad, alpha=-lr)

        total_loss += loss.item()

        if batch % 200 == 0 and batch > 0:
            cur_loss = total_loss / 200
            # #print('| epoch {:3d} | {:5d}/{:5d} batches | lr {:02.2f} | ms/batch {:5.2f} | '
            #         'loss {:5.2f} | ppl {:8.2f}'.format(
            #     epoch, batch, len(train_data) // args.bptt, lr,
            #     elapsed * 1000 / 200, cur_loss, math.exp(cur_loss)))
            total_loss = 0
            #start_time = time.time()
        if not True:
            break
    return model


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


def MarkivToString(startToken, length=None):
    """
    pass this a starting token and optionaly a lenght
    startToken= the token that will start the chain, either as a list or as a touple or as a string(yep, any of those should work)
    lenght the length of the result as an int(including inital token), if not specifyed or None will keep going until an end token is genorated
    returns strings
    uese the pickeled markov modle.
    """
    if isinstance(startToken, str):
        startTokenList = []
        startToken = startToken[2:len(startToken)-1]
        startToken = startToken.split(" ")
        for element in startToken:
            startTokenList.append(element)
        startToken = toupleAafy(startTokenList)

    generated = MarkovGen(startToken, length=length)
    output = "2/4, major, Engelska, "
    for elem in generated:
        output = output + "["
        for sumElemIndex in range(len(elem)):
            subElem = elem[sumElemIndex]
            output = output + str(subElem)
            if sumElemIndex<len(elem)-1:
                output = output + " "
            else:
                output = output + "], "
    output = output[0:len(output)-1]
    return output





if __name__ == "__main__":
    print("hellow world")
    #genSaveMarkov()
    #genList = MarkivToString((5, 2, 0), 20)
    #sprint(genList)
    #makeTrainingSet("./swedish_tunes_int.csv")
    modle = trainModleTransformer("./swedish_tunes_int.csv")
    




