# David Ariyibi, Williams College, daa1@williams.edu
# Katherine Blake, Williams College, kbb2@williams.edu
import csv
import pprint
import random

# file_ = 'example.csv'
# file_ = 'test_matrix.csv'
file_ = 'course professor evaluation form responses.csv'

remove_list = [0, 1, 2, 3, 4, 5, 6]
non_questions = [0, 1, 2, 3]
participant_col = 3
item_col = 4

# returns direct-translation 2d list dataset of input csv file
def csv_to_array(file_name, non_questions, id_index, item_index):
    array = []
    with open(file_name, 'rb') as csv_file:
        lines = csv.reader(csv_file)
        for row in lines:
            array.append(row)

    questions = array[0] # creates list of questions in order
    delete = 0
    for index in non_questions: # removes non-questions from question_list
        del questions[index - delete]
        delete += 1
        # del non_questions[non_questions.index(index)]
    del array[0] # removes row of questions from dataset

    participants = list_of_labels(array, id_index) # creates list of participants
    items = list_of_labels(array, item_index) # creates list of items (courses)

    return array, participants, items, questions

# returns two lists of csv-form responses, one for training, the other for testing
def bank_data(data, split): # split: expected percentage of responses put in training_data
    training_data = []
    test_data = []
	for row in data:
        if random.random() < split:
            training_data.append(row)
        else:
            test_data.append(row)

    return  training_data, test_data

# returns a list of things w/out repeats in order of appearance
def list_of_labels(array, index):
    labels = [] # empty list of labels
    for row in array:
        id_ = row[index]
        if id_ not in labels: # makes sure label is not already in list
            labels.append(id_)
    return labels

# pre:  assumes items is a list of all of the possible items.
#       assumes participants is a list of all participants.
#       blank is a boolean for setting empty cells: True sets with '', False with -1
# post: returns a 3d list of rows of people, columns of items,
#       and each intersecting cell has a list of ratings (responses to questions)
def array_to_3d(array, participants, items, id_index, item_index, blank):
    x = len(participants)
    y = len(items)
    z = len(array[0]) # number of questions per item
    if blank:
        array_3d = [[['' for k in xrange(z)] for j in xrange(y)] for i in xrange(x)] # creates empty 3d list for use in creating similarity graph
    else:
        array_3d = [[[ -1 for k in xrange(z)] for j in xrange(y)] for i in xrange(x)] # creates a copy for use in KNN_prediction

    for person in array:
        index_of_person = participants.index(person[id_index]) # finds corresponding row via index of name from participant_list
        index_of_item = items.index(person[item_index]) # finds corresponding col via index of item from item_list
        if blank:
            array_3d[index_of_person][index_of_item] = person
        else:
            array_3d[index_of_person][index_of_item] = person

    return array_3d

def remove_col(array_3d, remove_list):
    row = range(len(array_3d))
    col = range(len(array_3d[0]))
    dep = range(len(array_3d[0][0]))

    for person in row:
        for item in col:
            delete = 0
            for question in dep:
                if question in remove_list:
                    del array_3d[person][item][question - delete]
                    delete += 1

    return array_3d

def array_to_csv(array, file_name):
    with open(file_name + '.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting = csv.QUOTE_ALL)
        wr.writerow(array)

if __name__ == '__main__':
    (data, participant_list, item_list, question_list) = csv_to_array(file_, non_questions, participant_col, item_col)
    print matrix
