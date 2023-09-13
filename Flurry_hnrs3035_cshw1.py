import argparse
import re    
import pickle
import random

'''
Class for storing a word and its counts of subsequent words
totalOccurences = the total occurences of that word in the text
countDict = a dictionary with a key of the subsequent word and a value of the count of times that the key word occurs after the word represented by the object
'''
class word:    
    def __init__(self):
        self.totalOccurenecs=0
        self.countDict = {}
    
    #Adds an occurence of the word plus its subsequent word
    def add_occurence(self, next_word):
        #Updates the totalOccurences of the current word
        self.totalOccurenecs+=1
        
        #if the subsequent word is already in the count dict, increment by 1
        try:
            self.countDict[next_word]+=1
        #if the subsequent word is not in the count dict, initiate it to 1
        except:
            self.countDict[next_word]=1
    
    
    #Gets the next word after the current word by generating a random value in the range of occurences
    def get_next_word(self):
        #Generate a random value in the range [0, totalOccurences-1]
        rand = random.randint(0, self.totalOccurenecs-1)
        
        #Create a list of the counts of subsequent words
        countArray=list(self.countDict.values())
        
        #Find the index of the value that puts the random value less than 0
        index=0
        while(rand>0):
            rand-=countArray[index]
            index+=1
            
        #Use the index found in the previous step to return the word at that index
        length=len(countArray)    
        if(index==length):
            index-=1
        return list(self.countDict.keys())[index]
    
    #For trouble shooting to check that the counts were accurate
    def print_self(self):
        print(self.countDict)

'''
Class for storing the actual n gram model
dataSet = dict with key of string word and a value of word object as documented above
'''
class n_gram_model:
    def __init__(self):
        self.dataSet={}
    
    #Function for training the model
    def train(self, sample):
        #Convert the sample from array to a string
        sample = str(sample)
        
        #Clean the string to remove nonletter characters(I had to remove numbers to remove conflicts with KJV bible)
        cleanedSample = sample.replace("\\n", "")
        cleanedSample = re.sub(r'[^a-zA-Z. ]', '', cleanedSample)
        ' '.join(cleanedSample.split())
        cleanedSample = cleanedSample.replace(".", " . ")
        
        #split the sample to an array of individual words
        splitSample = cleanedSample.split(" ")
        
        #iterate over the array of words to update counts for the statistical model
        for x in range(0,len(splitSample)-1):
            #If the word already exists in data set then add the new occurence
            try:
                self.dataSet[splitSample[x]].add_occurence(splitSample[x+1])
            #If the word does not exist create it and add the initial occurence
            except:
                self.dataSet[splitSample[x]]=word()
                self.dataSet[splitSample[x]].add_occurence(splitSample[x+1])
                
    #Get the next n words after word
    def get_next_n_words(self, word, n):
        returnString=word + " "
        
        #Check if the initial word is in the dataset
        try:
            initial=self.dataSet[word].get_next_word()
        #Return a message if the word is not found in the set
        except KeyError:
            return "Word not found in sample set"
        
        #Iterate for n generating the word after word and adding it on to the list
        for x in range(0,int(n)):
            word = self.dataSet[word].get_next_word()
            returnString = returnString + word + " "
            
        return returnString
            
#Parse arguments 
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('control', metavar='control', help="Action to Perform")
parser.add_argument('--data', metavar='File Location', help="File of Data Corpus")
parser.add_argument('--save', metavar='save', help="Location to Save training Data")
parser.add_argument('--load', metavar='load', help="Location to load trained model from")
parser.add_argument('--word', metavar='fword', help="First word to use for prediction")
parser.add_argument('--nwords', metavar='nwords', help="Number of words to predict")
args = parser.parse_args()

#Create an instance of the model class
model = n_gram_model()

#Check we are in the main method
if __name__ == "__main__":
    #If control arg is train
    if(args.control == "train"):
        #Open and read the data set
        filex = open(args.data, "r", encoding="utf8")
        sample = filex.readlines()
        filex.close()

        #Use pickle to dump a copy of the model
        filey=open(args.save, "wb")
        model.train(sample.__str__())
        pickle.dump(model,filey)
        filey.close()
        
    #If control arg is predict 
    elif(args.control == "predict"):
            #Load Model
            filex = open(args.load, "rb")
            model = pickle.load(filex)
            
            #Print the output of n words for the loaded model
            print(model.get_next_n_words(args.word,args.nwords))
        