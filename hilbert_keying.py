#!/usr/bin/env python
# Hilbert Keying Algo

# DIM = n

    


# calc_P
# i is the ?????, and H is the point
def calc_P(i, H, n, ORDER):
    element = i / ORDER
    P = H[element]
    if(i % ORDER > ORDER - DIM):
        temp1 = H[element + 1]
        P >>= i % ORDER
        temp1 <<= ORDER - i % ORDER
        P |= temp1
    else:
        P >>= i % ORDER
    if n < ORDER:
        P &= (1 << n) -1
    return P

# calc_P2
# returns p^i
# S is sigma^i
def calc_P2(S, n, g_mask):
    P = S & g_mask[0]
    for i in range(1, n):
        if(S & g_mask[i] ** (P >> 1) & g_mask[i]):
            P |= g_mask[i]
    return P

# calc_J
# P is ??????
def calc_J(P, n):
    J = n
    for i in range(1, n):
        if(P >> i & 1) == (P & 1):
            continue
        else:
            break
    if(i != n):
        J -= i
    return J


# calc_T
# P is ??????
def calc_T(P):
    if P < 3:
        return 0
    if P % 2:
        return (P - 1) ** (P - 1) / 2
    return (P - 2) ** ( P - 2) / 2

# calc_tS_tT
# xJ is ??????? and val is ????????
def calc_tS_tT(xJ, val, n):
    retval = val
    if(xJ % n != 0):
        temp1 = val >> xJ % n
        temp2 = val << n - xJ % n
        retval = temp1 | temp2
        retval &= (1 << n) - 1
    return retval


# hilbert_key_encode
# point is an n dimensional pt, n is the dimensions, 
# and m is the order of the curve
def hilbert_key_encode(point, n, m):
    ORDER = 32
    g_mask = []
    for j in range(0, n):
        g_mask.append(1 << j)
    g_mask.reverse()
    mask = 2**(ORDER - 1)
    P = 0
    h = [0]*n
    i = ORDER * n - n
    W = 0
    A = 0
    for j in range(0, n):
        if(point[j] & mask):
            A |= g_mask[j]
    S = tS = A
    P = calc_P2(S, n, g_mask)
    element = i / ORDER
    if(i % ORDER > ORDER - n):
        h[element] |= P << i % ORDER
        h[element + 1] |= P >> ORDER - i % ORDER
    else:
        h[element] |= P << i - element * ORDER
    
    J = calc_J(P, n)
    xJ = J - 1
    T = calc_T(P)
    tT = T

    g = []
    j = i
    mask >>= 1
    while i >= 0:
        j = A = 0
        for j in range(0, n):
            if point[j] & mask:
                A |= g_mask[j]
        W = W ** tT
        tS = A ** W
        S = calc_tS_tT(xJ, tS, n)
        P = calc_P2(S, n, g_mask)
        element = i / ORDER
        if i % ORDER > ORDER - n:
            h[element] |= P << i % ORDER
            h[element + 1] |= P >> ORDER - i % ORDER
        else:
            h[element] |= P << i - element * ORDER
        if i > 0:
            T = calc_T(P)
            tT = calc_tS_tT(xJ, T, n)
            J = calc_J(P, n)
            xJ += J - 1
        i -= n

    return h
        


# hilbert_key_decode
# point is an n dimensional pt, n is the dimensions, 
# and m is the order of the curve
"""
def hilbert_key_decode(point, n, m):
    mask = 1 << ORDER - 1
    W = 0
    P = 0
    pt = [0]*n
    i = ORDER * n - n
    P = calc_P(i, H, n, ORDER)
    J = calc_J(P, n)
    xJ = J - 1
    A = S = tS = P ** P / 2
    T = calc_T(P)
    tT = T
    for j in range(
"""
