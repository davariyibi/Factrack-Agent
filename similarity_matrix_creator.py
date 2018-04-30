# David Ariyibi, Williams College, daa1@williams.edu
# Katherine Blake, Williams College, kbb2@williams.edu
import math
import pprint

example_matrix = [[[2, 6, 8, 6, 9], [2, 5, 5, 5, 0], [1, 3, 8, 8, 7], [2, 1, 4, 5, 8], [3, 2, 0, 6, 9]],
                  [[3, 2, 0, 6, 9], [2, 1, 4, 5, 8], [5, 6, 7, 4, 7], [2, 5, 5, 5, 0], [2, 6, 8, 6, 9]]]
# example_matrix = [[[2, 6, 8, 6, 9], [2, 5, 5, 5, 0], ['', '', '', '', '']],
                #   [[3, 2, 0, 6, 9], [2, 1, 4, 5, 8], [5, 6, 7, 4, 7]]]

file_ = 'test_matrix.csv'
test_matrix = []

def create_sim_matrix_3d(input_3d_array, remove_list_q, isItem):
    if isItem:
        length = range(len(input_3d_array[0]))
    else:
        length = range(len(input_3d_array[0][0]))
    sim_matrix_list = ['' for x in length]

    for index in length:
        if isItem:
            sim_matrix_list[index] = (create_sim_matrix(array_3d_to_2d_i(input_3d_array, index, remove_list_q)))
        elif index not in remove_list_q:
            sim_matrix_list[index] = (create_sim_matrix(array_3d_to_2d_q(input_3d_array, index)))

    return sim_matrix_list

# post: returns a symmetrical similarity matrix (2D list) of Pearson correlation coefficients between participants
def create_sim_matrix(input_array):
    row = range(len(input_array))
    col = range(len(input_array[0]))
    coeff = [['' for x in row] for y in row] # creates an empty similarity matrix

    for i in row: # person i
        coeff[i][i] = 1.0
        for j in row: # person j
            if (i < j):
                i_avg = avg_score(input_array[i], col)
                j_avg = avg_score(input_array[j], col)
                sum_numer = 0.0 # holds the sum in the numerator
                sum_denom_i = 0.0 # holds the sum for i in the denominator
                sum_denom_j = 0.0 # holds the sum for j in the denominator

                for k in col: # loops through all items 'k' being rated
                    i_rating = input_array[i][k]
                    j_rating = input_array[j][k]
                    if((i_rating is not '') and (j_rating is not '')): # if both people have rated item
                        i_diff = int(i_rating) - i_avg
                        j_diff = int(j_rating) - j_avg
                        sum_numer += (i_diff * j_diff)
                        sum_denom_i += (i_diff**2)
                        sum_denom_j += (j_diff**2)

                denom_total = math.sqrt(sum_denom_i * sum_denom_j)
                if denom_total != 0: # to temporarily solve 'divide by 0' problem
                    coeff[i][j] = sum_numer / denom_total # adds coefficient to similarity matrix
                else:
                    coeff[i][j] = 0
                coeff[j][i] = coeff[i][j] # makes similarity matrix symmetrical

    return coeff

# post: returns an 2D list for a specific question
def array_3d_to_2d_q(input_3d_array, question_index):
    row = range(len(input_3d_array)) # number of participants
    col = range(len(input_3d_array[0])) # number of total items
    array_2d = [['' for y in col] for x in row] # creates an empty 2D list for a specific question

    for person in input_3d_array: # for every person in the array
        for item in person: # for every item for each person
            array_2d[input_3d_array.index(person)][person.index(item)] = item[question_index] # assign rating in index position

    return array_2d

# post: returns an 2D list for a specific item
def array_3d_to_2d_i(input_3d_array, item_index, remove_list_i):
    r_length = len(remove_list_i)
    row = range(len(input_3d_array)) # number of participants
    col = range(len(input_3d_array[0][0]) - r_length) # number of total questions
    array_2d = [['' for y in col] for x in row] # creates an empty 2D list for a specific question

    for person in input_3d_array: # for every person in the array
        person_index = input_3d_array.index(person)
        array_2d[person_index] = input_3d_array[person_index][item_index]
        del array_2d[person_index][0:r_length]

    return array_2d

# post: returns a similarity matrix which is an average of a list of weighted similarity matricies
def combine_sim(graph_list, remove_list, weight_list):
    start_index = len(remove_list) # sections of ratings may be skipped due to irrelevance, we must combine at a different starting point
    num_of_graphs = range(len(graph_list[start_index][0]))
    combined_graph = [[0 for x in num_of_graphs] for y in num_of_graphs]
    # weight_list = weight_labels(graph_list, remove_list)

    for graph in graph_list: # adds all corresponding coefficients
        graph_index = graph_list.index(graph)
        for person in graph:
            person_index = graph.index(person)
            for item in person:
                item_index = person.index(item)
                combined_graph[person_index][item_index] += (weight_list[graph_index] * item)
                graph[person_index][item_index] = '' # clears old graph in order to make correct indexing

    total_weight = sum(weight_list)
    for person in combined_graph: # divides by number of
        person_index = combined_graph.index(person)
        for item in person:
            item_index = person.index(item)
            combined_graph[person_index][item_index] = (item + 0.0) / total_weight

    return combined_graph

# # post: returns list of ints with indecies corresponding to matrices in list of similarity matrix.
# #       determines the weight of each matrix on the final matrix.
# def weight_labels(graph_list, remove_list):
#     graph_length = range(len(graph_list))
#     weight_list = [0 for x in graph_length]
#     for graph in graph_list:
#         index = graph_list.index(graph)
#         if index in remove_list: # these are unwanted
#             weight_list[index] = 0
#         # elif statements can be added to give certain questions/items/etc. certain weights
#         else:
#             weight_list[index] = 1 # we do not yet have string parser to change strings to numbers
#
#     return weight_list

# post: returns average score for a given person
def avg_score(input_row, column_length):
    sum_of_scores = 0.0
    num_of_scores = 0.0
    for i in column_length:
        if input_row[i] is not '': # averages over items rated, not total items
            sum_of_scores += int(input_row[i])
            num_of_scores += 1

    if num_of_scores == 0: # in case participant has no response for item
        return 0
    else:
        return sum_of_scores / num_of_scores

# post: returns specific similarity matrix from list for a given index
def get_sim_matrix(graph_list, index):
    return graph_list[index]

# post: returns list of matricies with all numbers in absolute value
def abs_sim_3d(matrix_list):
    abs_matrix_list = []
    for matrix in matrix_list:
        abs_matrix_list.append(abs_sim_2d(matrix))
    return abs_matrix_list

# post: returns matrix with all entries in absolute value
def abs_sim_2d(matrix):
    abs_matrix = []
    for person in matrix:
        person_index = matrix.index(person)
        abs_matrix.append(map(abs, matrix[person_index]))
    return abs_matrix

if __name__ == '__main__':
    test_matrix, participant_list, item_list, question_list = csv_to_array(file_)
    pprint.pprint(test_matrix)
    pprint.pprint(create_sim_matrix(test_matrix))
    # pprint.pprint(combine_sim(example_matrix))
    # pprint.pprint(create_sim_matrix_3d(example_matrix, []))
