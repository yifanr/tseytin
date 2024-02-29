from pysat.solvers import Maplesat

num = 4

solver = Maplesat()

binary = bin(num)[2:]
print(binary)

print(len(binary))

bits1 = [i + 1 for i in range(len(binary))]
bits2 = [i + len(binary) + 1 for i in range(len(binary))]

for i in range((len(binary) + 1)//2):
    # pallindrome via xor's between pairs of mirrored bits
    solver.add_clause([-bits1[i], bits1[len(binary) - i - 1]])
    solver.add_clause([bits1[i], -bits1[len(binary) - i - 1]])
    solver.add_clause([-bits2[i], bits2[len(binary) - i - 1]])
    solver.add_clause([bits1[2], -bits2[len(binary) - i - 1]])