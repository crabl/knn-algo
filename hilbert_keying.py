#!/usr/bin/env python
# Hilbert Keying Algo

# DIM = n

    


# calc_P
# i is the ?????, and H is the point
def calc_P(i, H):

# calc_P2
# returns p^i
# S is sigma^i
def calc_P2(S):


# calc_J
# P is ??????
def calc_J(P):


# calc_T
# P is ??????
def calc_T(P):


# calc_tS_tT
# xJ is ??????? and val is ????????
def calc_tS_tT(xJ, val):


# hilbert_key_encode
# point is an n dimensional pt, n is the dimensions, 
# and m is the order of the curve
def hilbert_key_encode(point, n, m):
    g_mask = []
    for j in range(0, n):
        g_mask.append(1 << j)
    g_mask.reverse()
    mask = 2**(ORDER - 1)
    P = 0
    h = [0]*n
    i = ORDER * n - n
    A = 0
    for j in range(0, n):
        if(point[j] & mask):
            A |= g_mask[j]
    S = tS = A
    P = calc_P2(S)
    element = i / ORDER
    if(i % ORDER > ORDER - n):
        h[element] |= P << i % ORDER
        h[element + 1] |= P >> ORDER - i % ORDER
    else:
        h[element] |= P << i - element * ORDER
    if i > 0:
        T = calc_T(P)
        tT = calc_tS_tT(xJ, T)
        J = calc_J(P)
        xJ += J - 1
    return h
        


# hilbert_key_decode
# point is an n dimensional pt, n is the dimensions, 
# and m is the order of the curve
def hilbert_key_decode(point, n, m):
