import sys 
import csv
import math

class ProbabilityInformation:
    def __init__(self):
        #key: class [0-9] 
        #value: 2d list to store data for each pixel 
        self.class_probabilities = self.get_dict_from_text()
        #self.init_probability_dict()
        #self.populate_data()
        self.total_labels = 1000
        self.generate_probabilities()
        self.solutions = []
        self.calculate_MAP()

    def init_probability_2d(self):
        """
        Creates 2d list for each value in the class_probabilities. 28x28
        """
        retval = []
        for a in range(0,28):
            retval.append([])
            for b in range(0,28):
                #first element: # of '+', second element: # of '#', third element: # of ' ', fourth element: total test elements
                retval[a].append([0,0,0,0])
        return retval

    def init_probability_dict(self):
        """Initializes class dictionary to have each class map to 2d lists"""
        for x in xrange(0,10):
            self.class_probabilities[x] = self.init_probability_2d()
    
    def get_dict_from_text(self):
        with open('./accurate_statistics_dict.txt', 'r') as inf:
            return eval(inf.read())

    def populate_data(self):
        """
        Insert statistics into the 2d lists of lists based on test images
        Only need to run this once to obtain data
        TODO: remove the fourth element of the list. it is useless
        """
        training_labels = open('./digitdata/traininglabels', 'r')
        training_images = open('./digitdata/trainingimages', 'r')
        count = 0
        with training_images as ti:
            data = list(csv.reader(ti))
            for elem in data:
                print elem
            data = [i for i in data if i]
        for label in training_labels:
            l = 0
            while l < 28:
                coord = count + l
                w = 0
                while w < 28:
                    int_label = int(label)
                    if data[coord][0][l] == "+":
                        self.class_probabilities[int_label][l][w][0] += 1
                    if data[coord][0][l] == "#":
                        self.class_probabilities[int_label][l][w][1] += 1
                    if data[coord][0][l] == " ":
                        self.class_probabilities[int_label][l][w][2] += 1                        
                    w += 1
                l += 1
            count += 28 
        print self.class_probabilities

    def generate_probabilities(self):
        """
        Replace the dictionary's list elements with probabilities
        """
        k = 1
        v= 3
        for g in self.class_probabilities:
            for l in range(0,28):
                for w in range(0,28):
                    curr_list = self.class_probabilities[g]
                    total = float(curr_list[l][w][0] + curr_list[l][w][1] + curr_list[l][w][2])
                    curr_list[l][w][0] = (float(curr_list[l][w][0])+k)/(total + k*v) 
                    curr_list[l][w][1] = (float(curr_list[l][w][1])+k)/(total + k*v)
                    curr_list[l][w][2] = (float(curr_list[l][w][2])+k)/(total + k*v)


    def calculate_MAP(self):
        """
        In each test image, calculates the sum of the logs of the probabilities for each class [0-9]. 
        Appends the class with the highest sum to the solutions list for each image
        """
        testing_images = open('./digitdata/testimages', 'r')
        with testing_images as ti:
            data = list(csv.reader(ti))
            data = [i for i in data if i]
        count = 0
        #loop through all the test images
        for j in range(0,1000):
            classification_dict = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}  
            l = 0
            while l < 28:
                w = 0
                coord = count + l
                while w < 28:
                    if data[coord][0][w] == "+":
                        for z in range(0,10):
                            classification_dict[z] += math.log(self.class_probabilities[z][l][w][0]) 
                    elif data[coord][0][w] == "#":
                        for z in range(0,10):
                            classification_dict[z] += math.log(self.class_probabilities[z][l][w][1]) 
                    elif data[coord][0][w] == " ":
                        for z in range(0,10):
                            classification_dict[z] += math.log(self.class_probabilities[z][l][w][2]) 
                    w += 1
                l += 1
            count += 28
            #print classification_dict
            self.solutions.append(max(classification_dict, key=classification_dict.get))

def main():
    pinfo = ProbabilityInformation()
    print pinfo.class_probabilities
    #print pinfo.solutions
    #print len(pinfo.solutions)

if __name__ == "__main__":
    main()
