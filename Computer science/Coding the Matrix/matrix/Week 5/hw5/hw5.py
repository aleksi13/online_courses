# version code 941
# Please fill out this stencil and submit using the provided submission script.

from vecutil import list2vec
from solver import solve
from independence import rank
from matutil import listlist2mat, coldict2mat, mat2coldict, mat2rowdict, identity, rowdict2mat
from mat import Mat
from GF2 import one
from vec import Vec
from triangular import triangular_solve



## Problem 1
w0 = list2vec([1,0,0])
w1 = list2vec([0,1,0])
w2 = list2vec([0,0,1])

v0 = list2vec([1,2,3])
v1 = list2vec([1,3,3])
v2 = list2vec([0,3,3])

# Fill in exchange_S1 and exchange_S2
# with appropriate lists of 3 vectors

exchange_S0 = [w0, w1, w2]
exchange_S1 = [w0, w1, v2]
exchange_S2 = [v0, w1, v2]
exchange_S3 = [v0, v1, v2]



## Problem 2
w0 = list2vec([0,one,0])
w1 = list2vec([0,0,one])
w2 = list2vec([one,one,one])

v0 = list2vec([one,0,one])
v1 = list2vec([one,0,0])
v2 = list2vec([one,one,0])

exchange_2_S0 = [w0, w1, w2]
exchange_2_S1 = [w0, w1, v2]
exchange_2_S2 = [v0, w1, v2]
exchange_2_S3 = [v0, v1, v2]



## Problem 3

def vec2rep(veclist, v):
    '''
    Input:
        - veclist: a list of vectors (as instances of your Vec class)
        - v: a vector (as Vec instance) with domain set(range(len(veclist)))
             with v in the span of set(veclist).
    Output:
        Vec instance u whose coordinate representation w.r.t. veclist is v
    Example:
        >>> a0 = Vec({'a','b','c','d'}, {'a':1})
        >>> a1 = Vec({'a','b','c','d'}, {'b':1})
        >>> a2 = Vec({'a','b','c','d'}, {'c':1})
        >>> vec2rep([a0,a1,a2], Vec({'a','b','c','d'}, {'a':3, 'c':-2})) == Vec({0, 1, 2},{0: 3.0, 1: 0.0, 2: -2.0})
        True
    '''
    return solve(coldict2mat(veclist), v)

def morph(S, B):
    '''
    Input:
        - S: a list of distinct Vec instances
        - B: a list of linearly independent Vec instances
        - Span S == Span B
    Output: a list of pairs of vectors to inject and eject
    Example:
        >>> #This is how our morph works.  Yours may yield different results.
        >>> S = [list2vec(v) for v in [[1,0,0],[0,1,0],[0,0,1]]]
        >>> B = [list2vec(v) for v in [[1,1,0],[0,1,1],[1,0,1]]]
        >>> morph(S, B)
        [(Vec({0, 1, 2},{0: 1, 1: 1, 2: 0}), Vec({0, 1, 2},{0: 1, 1: 0, 2: 0})), (Vec({0, 1, 2},{0: 0, 1: 1, 2: 1}), Vec({0, 1, 2},{0: 0, 1: 1, 2: 0})), (Vec({0, 1, 2},{0: 1, 1: 0, 2: 1}), Vec({0, 1, 2},{0: 0, 1: 0, 2: 1}))]

    '''
    C = S.copy()
    list_to_return = []
    inject_list = []
    for v_inject in B:
        inject_list.append(v_inject)
        found = False
        for v_remove in C:
            if not found:
                u = vec2rep(C + inject_list, v_remove)
                if u * u > 1e-14:
                    found = True
                    C.remove(v_remove)
                    list_to_return.append ( (v_inject, v_remove) )
    return list_to_return

## Problem 4
# Please express each solution as a list of vectors (Vec instances)

row_space_1 = [Vec({0, 1, 2},{0: 1, 1: 2, 2: 0}), Vec({0, 1, 2},{0: 0, 1: 2, 2: 1})]
col_space_1 = [Vec({0, 1},{0: 1, 1: 0}), Vec({0, 1},{0: 0, 1: 1}) ]

row_space_2 = [Vec({0, 1, 2, 3},{0: 1, 1: 4, 2: 0, 3: 0}), Vec({0, 1, 2, 3},{0: 0, 1: 2, 2: 2, 3: 0}), Vec({0, 1, 2, 3},{0: 0, 1: 0, 2: 1, 3: 1}) ]
col_space_2 = [Vec({0, 1, 2},{0: 1, 1: 0, 2: 0}), Vec({0, 1, 2},{0: 0, 1: 2, 2: 1}), Vec({0, 1, 2},{0: 0, 1: 0, 2: 1})]

row_space_3 = [Vec({0},{0: 1})]
col_space_3 = [Vec({0, 1, 2},{0: 1, 1: 2, 2: 3})]

row_space_4 = [Vec({0, 1},{0: 1, 1: 0}), Vec({0, 1},{0: 2, 1: 1})]
col_space_4 = [Vec({0, 1, 2},{0: 1, 1: 2, 2: 3}), Vec({0, 1, 2},{0: 0, 1: 1, 2: 4})]



## Problem 5
def my_is_independent(L): 
    '''
    input:  A list, L, of Vecs
    output: A boolean indicating if the list is linearly independent
    
    >>> L = [Vec({0, 1, 2},{0: 1, 1: 0, 2: 0}), Vec({0, 1, 2},{0: 0, 1: 1, 2: 0}), Vec({0, 1, 2},{0: 0, 1: 0, 2: 1}), Vec({0, 1, 2},{0: 1, 1: 1, 2: 1}), Vec({0, 1, 2},{0: 1, 1: 1, 2: 0}), Vec({0, 1, 2},{0: 0, 1: 1, 2: 1})]
    >>> my_is_independent(L)
    False
    >>> my_is_independent(L[:2])
    True
    >>> my_is_independent(L[:3])
    True
    >>> my_is_independent(L[1:4])
    True
    >>> my_is_independent(L[0:4])
    False
    >>> my_is_independent(L[2:])
    False
    >>> my_is_independent(L[2:5])
    False
    '''
    return rank(L) == len(L)



## Problem 6

def is_superfluous(L, i):
    '''
    Input:
        - L: list of vectors as instances of Vec class
        - i: integer in range(len(L))
    Output:
        True if the span of the vectors of L is the same
        as the span of the vectors of L, excluding L[i].

        False otherwise.
    Examples:
        >>> a0 = Vec({'a','b','c','d'}, {'a':1})
        >>> a1 = Vec({'a','b','c','d'}, {'b':1})
        >>> a2 = Vec({'a','b','c','d'}, {'c':1})
        >>> a3 = Vec({'a','b','c','d'}, {'a':1,'c':3})
        >>> is_superfluous(L, 3)
        True
        >>> is_superfluous([a0,a1,a2,a3], 3)
        True
        >>> is_superfluous([a0,a1,a2,a3], 0)
        True
        >>> is_superfluous([a0,a1,a2,a3], 1)
        False
    '''
    D = L.copy()
    if i >= len(D):
        return False
    if len(D) <= 1:
        return False
    else:
        b = D.pop(i)
        u = solve(coldict2mat(D), b)
        residual = coldict2mat(D)*u - b
        if abs(residual * residual) < 10**(-14):
            return True
        else:
            return False

def subset_basis(T): 
    '''
    input: A list, T, of Vecs
    output: A list, S, containing Vecs from T, that is a basis for the
    space spanned by T.
    
    >>> a0 = Vec({'a','b','c','d'}, {'a':1})
    >>> a1 = Vec({'a','b','c','d'}, {'b':1})
    >>> a2 = Vec({'a','b','c','d'}, {'c':1})
    >>> a3 = Vec({'a','b','c','d'}, {'a':1,'c':3})
    >>> subset_basis([a0,a1,a2,a3]) == [Vec({'c', 'b', 'a', 'd'},{'a': 1}), Vec({'c', 'b', 'a', 'd'},{'b': 1}), Vec({'c', 'b', 'a', 'd'},{'c': 1})]
    True
    '''
    S = T.copy()
    done = False
    while not done:
        for k in range(len(S)):
            if is_superfluous(S, k):
                S.pop(k)
        done = my_is_independent(S)
    return S



## Problem 7
def my_rank(L): 
    '''
    input: A list, L, of Vecs
    output: The rank of the list of Vecs
    
    >>> my_rank([list2vec(v) for v in [[1,2,3],[4,5,6],[1.1,1.1,1.1]]])
    2
    '''
    return len(subset_basis(L))


## Problem 8
# Please give each answer as a boolean

only_share_the_zero_vector_1 = True
only_share_the_zero_vector_2 = True
only_share_the_zero_vector_3 = True



## Problem 9
def direct_sum_decompose(U_basis, V_basis, w):
    '''
    input:  A list of Vecs, U_basis, containing a basis for a vector space, U.
    A list of Vecs, V_basis, containing a basis for a vector space, V.
    A Vec, w, that belongs to the direct sum of these spaces.
    output: A pair, (u, v), such that u+v=w and u is an element of U and
    v is an element of V.
    
    >>> U_basis = [Vec({0, 1, 2, 3, 4, 5},{0: 2, 1: 1, 2: 0, 3: 0, 4: 6, 5: 0}), Vec({0, 1, 2, 3, 4, 5},{0: 11, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0}), Vec({0, 1, 2, 3, 4, 5},{0: 3, 1: 1.5, 2: 0, 3: 0, 4: 7.5, 5: 0})]
    >>> V_basis = [Vec({0, 1, 2, 3, 4, 5},{0: 0, 1: 0, 2: 7, 3: 0, 4: 0, 5: 1}), Vec({0, 1, 2, 3, 4, 5},{0: 0, 1: 0, 2: 15, 3: 0, 4: 0, 5: 2})]
    >>> w = Vec({0, 1, 2, 3, 4, 5},{0: 2, 1: 5, 2: 0, 3: 0, 4: 1, 5: 0})
    >>> direct_sum_decompose(U_basis, V_basis, w) == (Vec({0, 1, 2, 3, 4, 5},{0: 2.0, 1: 4.999999999999972, 2: 0.0, 3: 0.0, 4: 1.0, 5: 0.0}), Vec({0, 1, 2, 3, 4, 5},{0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0}))
    True
    '''
    UV = coldict2mat(U_basis+V_basis)    
    U = coldict2mat(U_basis)    
    V = coldict2mat(V_basis)    
    W = solve(UV,w)    
    Wu = list2vec([v for i, v in W.f.items() if i < len(U_basis)])    
    Wv = list2vec([v for i, v in W.f.items() if i >= len(U_basis)])    
    u = U * Wu
    v = V * Wv 
    return (u,v)



## Problem 10
def is_invertible(M): 
    '''
    input: A matrix, M
    outpit: A boolean indicating if M is invertible.
    
    >>> M = Mat(({0, 1, 2, 3}, {0, 1, 2, 3}), {(0, 1): 0, (1, 2): 1, (3, 2): 0, (0, 0): 1, (3, 3): 4, (3, 0): 0, (3, 1): 0, (1, 1): 2, (2, 1): 0, (0, 2): 1, (2, 0): 0, (1, 3): 0, (2, 3): 1, (2, 2): 3, (1, 0): 0, (0, 3): 0})
    >>> is_invertible(M)
    True
    '''
    return ( M.D[0] == M.D[1] ) and ( len(list(mat2coldict(M).values())) == rank(list(mat2coldict(M).values())) )

M = Mat(({0, 1, 2, 3}, {0, 1, 2, 3}), {(0, 1): 0, (1, 2): 1, (3, 2): 0, (0, 0): 1, (3, 3): 4, (3, 0): 0, (3, 1): 0, (1, 1): 2, (2, 1): 0, (0, 2): 1, (2, 0): 0, (1, 3): 0, (2, 3): 1, (2, 2): 3, (1, 0): 0, (0, 3): 0})
print( is_invertible(M) )

## Problem 11
def find_matrix_inverse(A):
    '''
    input: An invertible matrix, A, over GF(2)
    output: Inverse of A

    >>> M = Mat(({0, 1, 2}, {0, 1, 2}), {(0, 1): one, (1, 2): 0, (0, 0): 0, (2, 0): 0, (1, 0): one, (2, 2): one, (0, 2): 0, (2, 1): 0, (1, 1): 0})
    >>> find_matrix_inverse(M) == Mat(({0, 1, 2}, {0, 1, 2}), {(0, 1): one, (2, 0): 0, (0, 0): 0, (2, 2): one, (1, 0): one, (1, 2): 0, (1, 1): 0, (2, 1): 0, (0, 2): 0})
    True
    '''
    cols = []
    i = identity(A.D[0], one)
    i_cols = mat2coldict(i)
    for k in A.D[0]:
        cols.append( solve(A, i_cols[k]) )
    return coldict2mat(cols)



## Problem 12
def find_triangular_matrix_inverse(A): 
    '''
    input: An upper triangular Mat, A, with nonzero diagonal elements
    output: Inverse of A
    >>> A = listlist2mat([[1, .5, .2, 4],[0, 1, .3, .9],[0,0,1,.1],[0,0,0,1]])
    >>> find_triangular_matrix_inverse(A) == Mat(({0, 1, 2, 3}, {0, 1, 2, 3}), {(0, 1): -0.5, (1, 2): -0.3, (3, 2): 0.0, (0, 0): 1.0, (3, 3): 1.0, (3, 0): 0.0, (3, 1): 0.0, (2, 1): 0.0, (0, 2): -0.05000000000000002, (2, 0): 0.0, (1, 3): -0.87, (2, 3): -0.1, (2, 2): 1.0, (1, 0): 0.0, (0, 3): -3.545, (1, 1): 1.0})
    True
    '''
    cols = []
    i = identity(A.D[0], 1)
    i_cols = mat2coldict(i)
    for k in A.D[0]:
        cols.append( triangular_solve([ mat2rowdict(A)[k] for k in mat2rowdict(A) ], list(range(len(A.D[0]))), i_cols[k]) )
    return coldict2mat(cols)
