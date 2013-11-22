import sys
import math
import csv
import operator

class ClassifyDocuments:
    def __init__(self):
        #key: word, value: number of occurences
        self.training_dict = {}
        self.document_distributions = {}
        self.total_counts = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}
        self.init_training_dict() 
        self.solutions = []
        self.provided_solution = []
        self.confusion_matrix = []

    def init_training_dict(self):
        training_documents = open('./8newsgroups/8.trainingdata.txt', 'r')
        training_documents = training_documents.read()
        curr_key = 0
        for word in training_documents.split():
            if self.is_number(word):
                curr_key = int(word)
                if not curr_key in self.training_dict:
                    self.document_distributions[curr_key] = {}
                    self.training_dict[curr_key] = {}
            else:
                word_split = word.split(':')
                if word_split[0] in self.training_dict[curr_key]:
                    self.training_dict[curr_key][word_split[0]] += int(word_split[1])
                else:
                    self.training_dict[curr_key][word_split[0]] = int(word_split[1]) 
                self.total_counts[curr_key] += int(word_split[1])
        print self.total_counts

    
    def construct_probabilities(self):
        testing_documents = open('./8newsgroups/8.testingdata.txt', 'r')
        testing_documents = testing_documents.read()
        k = 1
        v = 58106
        classification_dict = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}  
        split_docs = testing_documents.split()
        curr_key = split_docs[0]
        flag = 0
        self.provided_solution.append(int(curr_key))
        for word in split_docs[1:len(split_docs)]:
            if self.is_number(word):
                curr_key =  int(word)
                self.provided_solution.append(int(word))
                #append the prev solution to solutions list
                self.solutions.append(max(classification_dict, key=classification_dict.get))
                classification_dict = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0}  
            if not self.is_number(word):
                coefficient = word.split(':')[1]
                text = word.split(':')[0]
                if text in self.document_distributions[int(curr_key)]:
                    self.document_distributions[int(curr_key)][text] += int(coefficient)
                else:
                    self.document_distributions[int(curr_key)][text] = int(coefficient)
                for x in range(0,8):
                    total = self.total_counts[x]
                    training_prob = 0
                    if text in self.training_dict[x]:
                        training_prob = float(self.training_dict[x][text] + k)/(total + k*v) 
                    else:
                        training_prob = float(k)/(total+k*v)   
                    classification_dict[x] += (math.log(float(coefficient)*training_prob)) 
            flag += 1 
        self.solutions.append(max(classification_dict, key=classification_dict.get))
    
    def is_number(self,val):
        """
        Check whether a given string is a number
        """
        try:
            float(val)
            return True
        except ValueError:
            return False

    def evaluation(self):
        self.init_confusion_matrix()
        num_correct = 0
        class_stats = {0:[0,0], 1:[0,0], 2:[0,0], 3:[0,0], 4:[0,0], 5:[0,0], 6:[0,0], 7:[0,0]}
        i = 0
        for x in range(0,len(self.provided_solution)-1):
            absolute_solution = self.provided_solution[x]
            class_stats[absolute_solution][1] += 1
            if absolute_solution == self.solutions[x]:
                class_stats[absolute_solution][0] += 1
                num_correct += 1
                self.confusion_matrix[absolute_solution][self.solutions[i]] += 1
            else:
                self.confusion_matrix[absolute_solution][self.solutions[i]] += 1
            i += 1
        for k in class_stats:
            print "Class " + str(k) + ": " + str(float(class_stats[k][0])/class_stats[k][1])
        print float(num_correct)/len(self.provided_solution)
        sorted_x = sorted(self.document_distributions[7].iteritems(), key=operator.itemgetter(1), reverse=True)
        #self.list_top_20(sorted_x)
        for l in range(0,8):
            for w in range(0,8):
                self.confusion_matrix[l][w] = float(self.confusion_matrix[l][w]) / class_stats[l][1]
        self.print_confusion_matrix()
    
    def print_confusion_matrix(self):
        s = [[str(e) for e in row] for row in self.confusion_matrix]
        lens = [len(max(col, key=len)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print '\n'.join(table)
    

    def gen_tags(self):
        print self.document_distributions[0]
        return ' '.join([('<font size="%d">%s</font>'%(self.document_distributions[7][x], x)) for (x, p) in self.document_distributions[7].items()])
        #return ' '.join([('<font size="%d">%s</font>'%(min(1+p*5/max(words.values()), 5), x)) for (x, p) in words.items()])

    def list_top_20(self, list_of_tuples):
        for x in range(0,20):
            print list_of_tuples[x][0] + ": " + str(list_of_tuples[x][1])

    def init_confusion_matrix(self):
        for l in range(0,8):
            self.confusion_matrix.append([0,0,0,0,0,0,0,0])






def main():
    cd = ClassifyDocuments()
    cd.construct_probabilities()
    print cd.solutions
    cd.evaluation()
    #print cd.document_distributions
    #print cd.gen_tags()

if __name__ == "__main__":
    main()
