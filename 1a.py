import re
from pysat.solvers import Maplesat
from pysat.card import *

# opening the file in read mode 
my_file = open("google-10000-english.txt", "r") 
  
# reading the file 
data = my_file.read()

words = data.split("\n")

my_file.close()

# opening the file in read mode 
my_file = open("message2.txt", "r") 
  
# reading the file 
data = my_file.read()

alien = re.split(r'[\W_]+', data)
print(alien)

solver = Maplesat()

alien_alphabet = {}
counter = 0
for word in alien:
    for char in word:
        if char not in alien_alphabet:
            alien_alphabet[char] = counter
            counter += 1

print(alien_alphabet)
num_alien_chars = len(alien_alphabet)

english_alphabet = {}
for i, char in enumerate('abcdefghijklmnopqrstuvwxyz'):
    english_alphabet[char] = i
print(english_alphabet)

variable_matrix = [[(num_alien_chars*i)+j+1 for j in range(num_alien_chars)] for i in range(26)]

for key in alien_alphabet:
    # each alien character must be mapped to at least one english character
    solver.add_clause([variable_matrix[i][alien_alphabet[key]] for i in range(26)])
    for j in range(26):
        for k in range(j+1, 26):
            # each alien character must be mapped to at most one english character
            solver.add_clause([-variable_matrix[j][alien_alphabet[key]], -variable_matrix[k][alien_alphabet[key]]])

num_vars = 26*num_alien_chars

counter = 0
for i, alien_word in enumerate(alien[:-1]):
    # keep track of each variable that corresponds to this alien word
    new_vars = []
    #tseitin encoding
    for word in words:
        if len(word) == len(alien_word):
            # define new auxiliary variable for two words matching after encoding - using tseitin encoding
            counter = counter + 1
            new_var = counter + num_vars
            if(new_var in [1736, 3116, 3846, 4948, 6073, 7536, 7583, 7957, 8042, 9512, 10295, 11632, 12323, 13410, 13805, 14941, 16317, 16710, 17103, 18352, 18900, 19300, 20595, 20630, 21756, 21803, 22177, 22854, 24232, 24736, 26097, 27222, 28685, 28732, 29282, 30575, 31260, 31644, 32499, 33837, 34221, 35076, 36414, 36798, 37653, 38979, 40362, 41432, 42195, 42844, 43975, 44373, 45625, 46413, 46878, 47934, 48323, 49008, 49392, 50247, 51570, 52706, 54083, 55205, 55881, 56426, 57395, 57917, 59314, 59987, 61357, 62482, 64172, 65072, 66205, 66880, 67265, 67950, 68517, 69839, 70548, 72027, 73153, 73692, 75037, 76541, 77516, 79026, 80149, 81285, 82662, 84013, 85293, 86867, 87924, 88671, 89753, 90849, 91982, 93368, 93752, 94607, 95945, 96329, 97184, 98522, 98906, 99761]):
                print(word)
            new_vars.append(new_var)
            solver.add_clause([new_var] + [-variable_matrix[english_alphabet[word[i]]][alien_alphabet[alien_word[i]]] for i in range(len(word))])
            for i in range(len(word)):
                solver.add_clause([-new_var, variable_matrix[english_alphabet[word[i]]][alien_alphabet[alien_word[i]]]])
    # each alien word must be mapped to at least one english word
    solver.add_clause(new_vars)

print(solver.solve())
positive_vars = []
for i in solver.get_model():
    if i>0:
        positive_vars.append(i)
print(positive_vars)
alien_alphabet_reverse = {v: k for k, v in alien_alphabet.items()}
english_alphabet_reverse = {v: k for k, v in english_alphabet.items()}
for var in positive_vars:
    x = var-1
    print(alien_alphabet_reverse[x%num_alien_chars], english_alphabet_reverse[x//num_alien_chars])