import numpy as np
from heapq import nlargest

# Pretend sample dataset to test with
test = [[[1, 1, 2, 3], [4, 5, 2, 3]],
       [[-1, -1, -1, -1], [5, 1, 3, 4]],
       [[3, 3, 4, 5], [1, 2, 4, 5]],
       [[4, 4, 5, 1], [-1, -1, -1, -1]]]

# Pretend sample similarity matrix to test with
test2 = [[1, .60, .25, .30],
        [.60, 1, .90, .75],
        [.25, .45, 1, .55],
        [.30, .75, .55, 1]]

'''  P1    P2     P3    P4      Same similarity matrix as above
P1   1    .60    .25   .30
P2  .60    1     .90   .75
P3  .25   .45     1    .55
P4  .30   .75    .55    1
'''
# Another pretend sample similarity matrix to test with
board_example = [[1, .60, .75, .80, .90],
                [.60, 1, .50, .33, .45],
                [.75, .5, 1, .25, .85],
                [.80, .33, .25, 1, .10],
                [.90, .45, .89, .10, 1]]

# Testing data from Lexi
sample = [[[3, 1, 4, 2, 1, 5, 2, 1, 1, 1, 1, 3], [2, 5, 3, 1, 1, 5, 2, 1, 1, 5, 5, 5],
[5, 5, 4, 1, 1, 5, 2, 1, 1, 5, 5, 5]],
[[5, 5, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4], [4, 5, 3, 2, 2, 2, 4, 3, 3, 4, 4, 3],
[3, 2, 4, 4, 4, 3, 3, 3, 3, 2, 2, 4]],
[[3, 4, 3, 4, 3, 3, 4, 3, 4, 3, 4, 3], [1, 1, 5, 5, 5, 5, 5, 5, 1, 1, 1, 1],
[4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3]],
[[5, 3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 3], [4, 5, 3, 4, 3, 5, 5, 4, 1, 5, 3, 4],
[4, 3, 3, 3, 2, 3, 3, 3, 4, 3, 3 ,3]],
[[4, 5, 3, 2, 1, 2, 2, 4, 2, 4, 4, 4], [5, 5, 3, 1, 1, 4, 5, 5, 4, 5, 5, 5],
[4, 5, 3, 4, 3, 2, 4, 4, 3, 3, 4, 4]],
[[2, 4, 2, 3, 4, 3, 2, 3, 4, 3, 2, 3], [4, 5, 4, 4, 3, 3, 4, 3, 3, 4, 4, 3],
[3, 2, 3, 4, 3, 3, 3, 2, 2, 4, 4, 3]],
[[3, 4, 3, 4, 4, 3, 4, 3, 3, 4, 4, 4], [4, 3, 3, 3, 4, 3, 3, 4, 3, 3, 4, 3],
[4, 3, 3, 3, 3, 3, 4, 2, 3, 3, 3, 3]],
[[4, 4, 3, 3, 2, 4, 4, 3, 3, 2, 3, 3], [5, 5, 4, 4, 2, 2, 4, 4, 2, 4, 4, 4],
[4, 4, 3, 3, 3, 2, 4, 3, 3, 4, 4, 4]],
[[4, 5, 4, 3, 3, 2, 3, 2, 2, 2, 4, 4], [4, 5, 3, 4, 4, 3, 3, 3, 2, 1, 1, 1],
[4, 3, 4, 3, 4, 3, 3, 4, 4, 3, 4 ,4]],
[[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], [5, 5, 2, 1, 1, 5, 5, 1, 5, 5, 5, 5],
[5, 5, 2, 1, 1, 5, 5, 1, 5, 5, 5, 4]]
]

# Similarity matrix generated from Lexi's sample data
sample_sim = [[1.0, -0.01594912489811881, -0.49550063964008184, 0.30193155535448557, 0.2743890835242543, 0.2782247322294236, -0.0265832166132495, 0.302538713938059, -0.26240293008063853, 0.6298327211154345],
 [-0.01594912489811881, 1.0, -0.15715330950248182, 0.01750008452277045, 0.25308050377371205, 0.3614720195339099, -0.009276773134741378, 0.1438420135091252, 0.14009703512032895, -0.038190912244028874],
 [-0.49550063964008184, -0.15715330950248182, 1.0, 0.12172749939637392, -0.3147554710623728, -0.4057961479321209, 0.04879500364742665, -0.4252975309317527, 0.14648836282380917, -0.5152145857759565],
 [0.30193155535448557, 0.01750008452277045, 0.12172749939637392, 1.0, 0.19502748763659333, 0.07539743296292331, 0.05400073251697762, 0.3018138474568839, 0.17587359559193055, 0.349776677636259],
 [0.2743890835242543, 0.25308050377371205, -0.3147554710623728, 0.19502748763659333, 1.0, 0.013169077329687084, 0.046383865673706955, 0.5705226995917018, -0.20828015703998218, 0.37513175707208507],
 [0.2782247322294236, 0.3614720195339099, -0.4057961479321209, 0.07539743296292331, 0.013169077329687084, 1.0, 0.025031742681132604, 0.46057919883758347, 0.0544493892263658, 0.11227217828476801],
 [-0.0265832166132495, -0.009276773134741378, 0.04879500364742665, 0.05400073251697762, 0.046383865673706955, 0.025031742681132604, 1.0, 0.2377334195982595, -0.05397126910508385, 0.10934121704162039],
 [0.302538713938059, 0.1438420135091252, -0.4252975309317527, 0.3018138474568839, 0.5705226995917018, 0.46057919883758347, 0.2377334195982595, 1.0, 0.08492097674510608, 0.27916806302686664],
 [-0.26240293008063853, 0.14009703512032895, 0.14648836282380917, 0.17587359559193055, -0.20828015703998218, 0.0544493892263658, -0.05397126910508385, 0.08492097674510608, 1.0, -0.3203476604121912],
 [0.6298327211154345, -0.038190912244028874, -0.5152145857759565, 0.349776677636259, 0.37513175707208507, 0.11227217828476801, 0.10934121704162039, 0.27916806302686664, -0.3203476604121912, 1.0]]

sample_abs_sim = [[1.0, 0.01594912489811881, 0.49550063964008184, 0.30193155535448557, 0.2743890835242543, 0.2782247322294236, 0.0265832166132495, 0.302538713938059, 0.26240293008063853, 0.6298327211154345],
 [0.01594912489811881, 1.0, 0.15715330950248182, 0.01750008452277045, 0.25308050377371205, 0.3614720195339099, 0.009276773134741378, 0.1438420135091252, 0.14009703512032895, 0.038190912244028874],
 [0.49550063964008184, 0.15715330950248182, 1.0, 0.12172749939637392, 0.3147554710623728, 0.4057961479321209, 0.04879500364742665, 0.4252975309317527, 0.14648836282380917, 0.5152145857759565],
 [0.30193155535448557, 0.01750008452277045, 0.12172749939637392, 1.0, 0.19502748763659333, 0.07539743296292331, 0.05400073251697762, 0.3018138474568839, 0.17587359559193055, 0.349776677636259],
 [0.2743890835242543, 0.25308050377371205, 0.3147554710623728, 0.19502748763659333, 1.0, 0.013169077329687084, 0.046383865673706955, 0.5705226995917018, 0.20828015703998218, 0.37513175707208507],
 [0.2782247322294236, 0.3614720195339099, 0.4057961479321209, 0.07539743296292331, 0.013169077329687084, 1.0, 0.025031742681132604, 0.46057919883758347, 0.0544493892263658, 0.11227217828476801],
 [0.0265832166132495, 0.009276773134741378, 0.04879500364742665, 0.05400073251697762, 0.046383865673706955, 0.025031742681132604, 1.0, 0.2377334195982595, 0.05397126910508385, 0.10934121704162039],
 [0.302538713938059, 0.1438420135091252, 0.4252975309317527, 0.3018138474568839, 0.5705226995917018, 0.46057919883758347, 0.2377334195982595, 1.0, 0.08492097674510608, 0.27916806302686664],
 [0.26240293008063853, 0.14009703512032895, 0.14648836282380917, 0.17587359559193055, 0.20828015703998218, 0.0544493892263658, 0.05397126910508385, 0.08492097674510608, 1.0, 0.3203476604121912],
 [0.6298327211154345, 0.038190912244028874, 0.5152145857759565, 0.349776677636259, 0.37513175707208507, 0.11227217828476801, 0.10934121704162039, 0.27916806302686664, 0.3203476604121912, 1.0]]

# Checks whether a class rating is unanswered
def isBlank(class_rating, questions_num):
  # Creates an example of a unanswered class rating
  blank = [-1 for r in range(questions_num)]

  # Compares the class rating passed in to the unanswered class rating
  if np.array_equal(class_rating, blank):
    return True

# Returns the k-nearest neighbors for a given person based on the
# similarity matrix
def getKNN(k, person, sim_matrix): #person is zero indexed
  largest_coeffs = [] # Creates an empty list
  k_nearest = [] # Creates an empty list

  # Finds the k+1 largest PCCs between the person and everyone else
  largest_coeffs = nlargest(k+1, sim_matrix[person])

  # Stores the index of the PCC between the person and themselves
  index = largest_coeffs.index(1)
  del largest_coeffs[index] # Deletes the PCC between themselves

  # Goes through the sim_matrix and laregest PCCs to get the
  # person the PCC comes from
  for num in range(len(sim_matrix)):
    for coeff in largest_coeffs:
      if (sim_matrix[person][num] == coeff): # Checks if the PCCs are equal
        k_nearest.append(num+1) # Stores the persons with the k laregest PCCs in a list

  return k_nearest # Returns a list with the k-nearest neighbors with an index of 1

# Finds all the unanswered class ratings in the martrix
def findBlanks(ans_matrix):
  blanks = [] # Creates an empty list

  # Goes through all student/class pairings in 3D matrix and
  # checks for any unanswered class ratings
  for person in range(len(ans_matrix)):
    for class_ in range(len(ans_matrix[person])):
      if (isBlank(ans_matrix[person][class_], len(ans_matrix[person][class_]))):
        blanks.append((person+1, class_+1)) # Stores the person and class

  return blanks # Returns the student/class pairing that is unanswered

# Gets all the k-nearest student's answers for a given class
def getAnswers(class_, k_nearest, ans_matrix):
  class_ans = {} # Creates an empty dictionary

  # Goes through every person in the matrix and checks if they are
  # one of the k-nearest neighbors. If so, it makes sure the person's
  # class ratings are not unanswered
  for person in range(len(ans_matrix)):
    if (person in k_nearest):
      if (not isBlank(ans_matrix[person][class_], len(ans_matrix[person][class_]))):
        class_ans[person] = ans_matrix[person][class_] # Stores the class rating for the person

  return class_ans # Returns the given class rating for the k-nearest neighbors

# Gets the PCC for the k-nearest students
def getSimilarities(person, k_nearest, sim_matrix):
  sims = {} # Creates an empty dictionary
  k_nearest[:] = [x - 1 for x in k_nearest] # Subtracts one from k-nearest neighbors list

  # Goes through the PCCs for the a given student and checks if
  # the student is a k-nearest neighbor. If so, it will add their PCC
  # to the dictionary
  for num in range(len(sim_matrix[person])):
    if (num in k_nearest):
      sims[num] = sim_matrix[person][num] # Stores PCC for the student

  return sims # Returns the PCCs for the k-nearest neighbors

# Looks through the k-nearest students's PCC and checks if it is
# negative. If so, it will apply the equation y = 6 - x to change the
# student's PCC.
def flipSigns(similarities, class_ans):
  # Goes through the k-nearest students and checks if their PCC
  # is negative
  for person in similarities:
    if (similarities[person] < 0):

      # Goes through the individual class ratings to change the answer
      # using the above equation
      for rating in range(len(class_ans[person])):
        class_ans[person][rating] = 6 - int(class_ans[person][rating])

      similarities[person] = abs(similarities[person]) # Changes the PCC to be positive

# Applies the math involved in predicting an answer for a given student
def predict_ans(class_ans, k_nearest, similarities):
  prediction = [] # Creates an empty list
  total = 0

  # Goes through the PCCs for the k-nearest neighbors and adds them together
  for person in similarities:
    total += similarities[person]

  # Goes through the PCCs and divides them by the total
  for person in similarities:
    similarities[person] = similarities[person]/total

  # Goes through the k-nearest neighbors and multiplies them the new PCCs
  for person in k_nearest:
    new_ratings = [float(x) * similarities[person] for x in class_ans[person]]
    prediction.append(new_ratings) # Stores the ratings in the list

  # Returns one list with all the class ratings summed together
  return [sum(x) for x in zip(*prediction)]

# Finds missing class ratings for individuals and fills them with
# a predicted score using the k-nearest neighbors algorithm
def fillBlanks(ans_matrix, sim_matrix, abs_sim_matrix, k):
  blanks = findBlanks(ans_matrix) # Finds unanswered class rating in 3D matrix
  predictions = {} # Creates an empty dictionary

  # Goes thrugh all blanks and fills them using the above methods
  for tuple_ in blanks:
    person = tuple_[0] - 1 # Stores the person
    class_ = tuple_[1] - 1 # Stores the class

    k_nearest = getKNN(k, person, abs_sim_matrix) # Stores the k-nearest students

    # Stores the PCCs and class ratings for the k-nearest students
    similarities = getSimilarities(person, k_nearest, sim_matrix)
    class_ans = getAnswers(class_, k_nearest, ans_matrix)

    # Filps the answers of negative PCCs
    flipSigns(similarities, class_ans)

    # Stores the predicted answer for a given student/class pairing
    prediction = predict_ans(class_ans, k_nearest, similarities)

    # Adds the new prediction for a given person and class into the dictionary
    predictions[(person, class_)] = prediction
    ans_matrix[person][class_] = prediction # Modifies the 3D matrix with updated answers

  return (ans_matrix, predictions) # Returns the new 3D matrix and all changes made

#fillBlanks(sample, sample_sim, sample_abs_sim)
