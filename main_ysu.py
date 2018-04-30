# David Ariyibi, Williams College, daa1@williams.edu
# Katherine Blake, Williams College, kbb2@williams.edu
from data_parser import csv_to_array, array_to_3d, remove_col
from similarity_matrix_creator import create_sim_matrix_3d, combine_sim, abs_sim_2d
from KNN_prediction import fillBlanks
import pprint

input_file = 'course professor evaluation form responses.csv' # csv file: raw data
data = [] # 2D list: direct translation of input_file
participant_list = [] # list: list of participant IDs in order
item_list = [] # list: list of item (class) IDs in order
question_list = [] # list: list of response questions in order
dataset = [] # 3D list: 1st dim participants, 2nd dim items, 3rd dim time stamp + IDs + responses
dataset1 = [] # 3D list: copy of dataset, but with blank responses filled with -1
dataset1_res = [] # 3D list: dataset1 with only responses
sim_matrix_list_i = [] # 3D list: list of item-based similarity matricies made from dataset
sim_matrix_i = [] # 2D list: item-averaged similarity matrix made from sim_matrix_list_i
abs_sim_matrix_i = [] # 2D list: sim_matrix_i with absolute value version of entries
full_dataset = [] # #D list:
predictions = [] # list of dict: (Katherine please add description)

# remove_list_q holds the indecies of the questions we are not using
# remove_list_i holds the indecies of the items we are not using
# non_questions holds the indecies of strings that are not questions but are in the row with the questions
# id_index is the column where participants list their identifying marker (i.e. name, nickname, etc.)
# item_index is the column where participnts list the iitem (class) they are awering questions on (rating)
def main(file_name, remove_list_q = [0, 1, 2, 3, 4, 5, 6], remove_list_i = [], non_questions = [0, 1, 2, 3], id_index = 3, item_index = 4):
    print 'Cleaning survey responses...'
    print 'Allocating info...'
    data, participant_list, item_list, question_list = csv_to_array(file_name, non_questions, id_index, item_index)

    print 'Creating full datasets: (\'\') and (-1)...'
    dataset = array_to_3d(data, participant_list, item_list, id_index, item_index, blank = True)
    dataset1 = array_to_3d(data, participant_list, item_list, id_index, item_index, blank = False)

    print 'Creating list of item-based similarity matricies...'
    sim_matrix_list_i = create_sim_matrix_3d(dataset, remove_list_q, isItem = True)

    print 'Creating item-averaged similarity matrix...'
    sim_matrix_i = combine_sim(sim_matrix_list_i, remove_list_i)

    print 'Creating dataset (-1) with only responses...'
    dataset1_res = remove_col(dataset1, remove_list_i)

    print 'Creating abs version of item-averaged similarity matrix...'
    abs_sim_matrix_i = abs_sim_2d(sim_matrix_i)

    print 'Checking for unanswered questions...'
    print 'Filling in unanswered questions...'
    # print 'Printing new dataset...'
    prediction = fillBlanks(dataset1_res, sim_matrix_i, abs_sim_matrix_i)
    full_dataset = prediction[0]
    predictions = prediction[1]

    print 'Printing filled answers...'
    print predictions

if __name__ == '__main__':
    main(input_file)

    # for a particular person, it returns a list of untaken classes and their scores???
