from vec import Vec
from mat import Mat
from mat import matrix_vector_mul
from bitutil import noise
from bitutil import str2bits, bits2str, bits2mat, mat2bits
from GF2 import one
from matutil import listlist2mat
from matutil import mat2coldict
from matutil import coldict2mat

## Task 1 part 1
""" Create an instance of Mat representing the generator matrix G. You can use
the procedure listlist2mat in the matutil module (be sure to import first).
Since we are working over GF (2), you should use the value one from the
GF2 module to represent 1"""
Gl = [ [ one, 0, one, one ], [ one, one, 0, one ], [ 0, 0, 0, one ], [ one, one, one, 0 ], [ 0, 0, one, 0 ], [ 0, one, 0, 0 ], [ one, 0, 0, 0 ] ]
G = listlist2mat(Gl)

## Task 1 part 2
# Please write your answer as a list. Use one from GF2 and 0 as the elements.
res = G * Vec( {0,1,2,3}, {0:one,1:0,2:0,3:one} )
encoding_1001 = [0, 0, one, one, 0, 0, one]

## Task 2
# Express your answer as an instance of the Mat class.
R = Mat( ( {0,1,2,3}, {0,1,2,3,4,5,6} ), {(0,6): one,(1,5): one,(2,4): one,(3,2): one} )

## Task 3
# Create an instance of Mat representing the check matrix H.
Hl = [ [0,0,0,one,one,one,one], [ 0,one,one,0,0,one,one], [one,0,one,0,one,0,one] ]
H = listlist2mat(Hl)


## Task 4 part 1
def find_error(e):
    """
    Input: an error syndrome as an instance of Vec
    Output: the corresponding error vector e
    Examples:
        >>> find_error(Vec({0,1,2}, {0:one}))
        Vec({0, 1, 2, 3, 4, 5, 6},{3: one})
        >>> find_error(Vec({0,1,2}, {2:one}))
        Vec({0, 1, 2, 3, 4, 5, 6},{0: one})
        >>> find_error(Vec({0,1,2}, {1:one, 2:one}))
        Vec({0, 1, 2, 3, 4, 5, 6},{2: one})    
    """
    for i in H.D[1]: 
        if (mat2coldict(H)[i] == e): 
            return( Vec( H.D[1], {i: one} ) )
    return( Vec( H.D[1], {} ) )
 

## Task 4 part 2
# Use the Vec class for your answers.
non_codeword = Vec({0,1,2,3,4,5,6}, {0: one, 1:0, 2:one, 3:one, 4:0, 5:one, 6:one})
error_vector = find_error(H * non_codeword)
code_word = non_codeword + error_vector
original = R * code_word


## Task 5
def find_error_matrix(S):
    """
    Input: a matrix S whose columns are error syndromes
    Output: a matrix whose cth column is the error corresponding to the cth column of S.
    Example:
        >>> S = listlist2mat([[0,one,one,one],[0,one,0,0],[0,0,0,one]])
        >>> find_error_matrix(S)
        Mat(({0, 1, 2, 3, 4, 5, 6}, {0, 1, 2, 3}), {(1, 2): 0, (3, 2): one, (0, 0): 0, (4, 3): one, (3, 0): 0, (6, 0): 0, (2, 1): 0, (6, 2): 0, (2, 3): 0, (5, 1): one, (4, 2): 0, (1, 0): 0, (0, 3): 0, (4, 0): 0, (0, 1): 0, (3, 3): 0, (4, 1): 0, (6, 1): 0, (3, 1): 0, (1, 1): 0, (6, 3): 0, (2, 0): 0, (5, 0): 0, (2, 2): 0, (1, 3): 0, (5, 3): 0, (5, 2): 0, (0, 2): 0})
    """
    return coldict2mat({ i: find_error(mat2coldict(S)[i]) for i in S.D[1] })


## Task 6
s = "I'm trying to free your mind, Neo. But I can only show you the door. You’re the one that has to walk through it."
P = bits2mat(str2bits(s))

## Task 7
C = G * P
bits_before = len(P.D[0])*len(P.D[1])
bits_after = len(C.D[0])*len(C.D[1])


## Ungraded Task
CTILDE = None

## Task 8
def correct(A):
    """
    Input: a matrix A each column of which differs from a codeword in at most one bit
    Output: a matrix whose columns are the corresponding valid codewords.
    Example:
        >>> A = Mat(({0,1,2,3,4,5,6}, {1,2,3}), {(0,3):one, (2, 1): one, (5, 2):one, (5,3):one, (0,2): one})
        >>> correct(A)
        Mat(({0, 1, 2, 3, 4, 5, 6}, {1, 2, 3}), {(0, 1): 0, (1, 2): 0, (3, 2): 0, (1, 3): 0, (3, 3): 0, (5, 2): one, (6, 1): 0, (3, 1): 0, (2, 1): 0, (0, 2): one, (6, 3): one, (4, 2): 0, (6, 2): one, (2, 3): 0, (4, 3): 0, (2, 2): 0, (5, 1): 0, (0, 3): one, (4, 1): 0, (1, 1): 0, (5, 3): one})
    """
    return A + find_error_matrix(H * A)


