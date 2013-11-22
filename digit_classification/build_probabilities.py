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
        self.solutions = []
        self.confusion_matrix = []

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
        """
        Initializes class dictionary to have each class map to 2d lists
        """
        for x in xrange(0,10):
            self.class_probabilities[x] = self.init_probability_2d()
   
    def init_confusion_matrix(self):
        for l in range(0,10):
            self.confusion_matrix.append([0,0,0,0,0,0,0,0,0,0])

    def get_dict_from_text(self):
        with open('./new_stats.txt', 'r') as inf:
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
            data = [i for i in data if i]
        for label in training_labels:
            l = 0
            while l < 28:
                coord = count + l
                w = 0
                while w < 28:
                    int_label = int(label)
                    if data[coord][0][w] == "+":
                        self.class_probabilities[int_label][l][w][0] += 1
                    if data[coord][0][w] == "#":
                        self.class_probabilities[int_label][l][w][1] += 1
                    if data[coord][0][w] == " ":
                        self.class_probabilities[int_label][l][w][2] += 1                        
                    w += 1
                l += 1
            count += 28 
        print self.class_probabilities

    def print_prob_dict(self):
        for g in self.class_probabilities:
            curr_list = self.class_probabilities[g]
            for l in range(0,28):
                for w in range(0,28):
                    for z in range(0,4):
                        txt = str(curr_list[l][w][z])
                        sys.stdout.write(txt + " ")
                print "\n\n"

    def print_confusion_matrix(self):
        s = [[str(e) for e in row] for row in self.confusion_matrix]
        lens = [len(max(col, key=len)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)
    
    def generate_probabilities(self):
        """
        Replace the dictionary's list elements with probabilities
        """
        k = 1
        v= 10
        for g in self.class_probabilities:
            curr_list = self.class_probabilities[g]
            for l in range(0,28):
                for w in range(0,28):
                    total = float(curr_list[l][w][0] + curr_list[l][w][1] + curr_list[l][w][2])
                    curr_list[l][w][0] = (float(curr_list[l][w][0])+k)/(total + k*v) 
                    curr_list[l][w][1] = (float(curr_list[l][w][1])+k)/(total + k*v)
                    curr_list[l][w][2] = (float(curr_list[l][w][2])+k)/(total + k*v)
                    curr_list[l][w][3] = curr_list[l][w][0] + curr_list[l][w][1] + curr_list[l][w][2]

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
            for l in range(0,28):
                coord = count + l
                for w in range(0,28):
                    if data[coord][0][w] == "+":
                        #iterate through each class. z is the class [0-9]
                        for z in range(0,10):
                            classification_dict[z] += math.log(self.class_probabilities[z][l][w][0]) 
                    elif data[coord][0][w] == "#":
                        for z in range(0,10):
                            classification_dict[z] += math.log(self.class_probabilities[z][l][w][1])
                    elif data[coord][0][w] == " ":
                        for z in range(0,10):
                            classification_dict[z] += math.log(self.class_probabilities[z][l][w][2])
            count += 28
            self.solutions.append(max(classification_dict, key=classification_dict.get))

    def evaluate_classifications(self):
        """
        Evaluates the accuracy of the digit classification. Builds a confusion matrix
        """
        test_labels = open('./digitdata/testlabels', 'r')
        self.init_confusion_matrix()
        i = 0
        class_stats = {0:[0,0], 1:[0,0], 2:[0,0], 3:[0,0], 4:[0,0], 5:[0,0], 6:[0,0], 7:[0,0], 8:[0,0], 9:[0,0]}
        total_correct = 0
        num_labels = 1000
        for label in test_labels:
            int_label = int(label)
            if int_label == self.solutions[i]:
                class_stats[int_label][0] += 1
                self.confusion_matrix[int_label][self.solutions[i]] += 1
            else:
                self.confusion_matrix[int_label][self.solutions[i]] += 1
            class_stats[int_label][1] += 1
            i += 1
        for k in class_stats:
            print "Class " + str(k) + ": " + str(float(class_stats[k][0])/class_stats[k][1])
            total_correct += float(class_stats[k][0])
        print "Overall Accuracy: " + str(total_correct/num_labels) 
        for l in range(0,10):
            for w in range(0,10):
                self.confusion_matrix[l][w] = float(self.confusion_matrix[l][w]) / class_stats[l][1]
        
        s = [[str(e) for e in row] for row in self.confusion_matrix]
        lens = [len(max(col, key=len)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)
        #self.print_confusion_matrix() 

def main():
    pinfo = ProbabilityInformation()
    pinfo.generate_probabilities()
    pinfo.calculate_MAP()
    print pinfo.solutions
    pinfo.evaluate_classifications()
    
if __name__ == "__main__":
    main()
