#!/usr/bin/env python
# Hilbert Keying Algo

# DIM = n

# calc_P
# i is a number, and H is the point
def calc_P(i, H, n, ORDER):
    MAX = 2 ** ORDER
    element = i / ORDER
    P = H[element]
    if(i % ORDER > ORDER - n):
        temp1 = H[element + 1]
        P /= 2 ** (i % ORDER)
        temp1 *= 2 ** (ORDER - i % ORDER)
        P %= MAX
        temp1 %= MAX
        P |= temp1
    else:
        P /= 2 ** (i % ORDER)
        P %= MAX
    if n < ORDER:
        P &= (2 ** n) - 1
    return P

# calc_P2
# returns p^i
# S is sigma^i
def calc_P2(S, n, g_mask, MAX):
    P = S & g_mask[0]
    for i in range(1, n):
        if(S & ((g_mask[i] ** (P/2))% MAX) & g_mask[i]):
            P |= g_mask[i]
    return P

# calc_J
# P is a number, n is the dimensions
def calc_J(P, n):
    J = n
    for i in range(1, n):
        if(P/(2 ** i) & 1) == (P & 1):
            continue
        else:
            break
    if(i != n):
        J -= i
    return J


# calc_T
# P is a number
def calc_T(P):
    if P < 3:
        return 0
    if P % 2:
        return ((P - 1) ^ (P - 1)) / 2
    return ((P - 2) ^ ( P - 2)) / 2

# calc_tS_tT
# xJ is ??????? and val is ????????
def calc_tS_tT(xJ, val, n, MAX):
    retval = val
    if(xJ % n != 0):
        temp1 = val / (2 ** xJ % n)
        temp2 = (val * (2 ** n - xJ % n)) % MAX
        retval = temp1 | temp2
        retval &= (2 ** n) - 1
    return retval


# hilbert_key_encode
# point is an n dimensional pt, n is the dimensions, 
# and m is the order of the curve
def hilbert_key_encode(n, m, point):
    pt = []
    for x in point:
        pt.append(x)
    ORDER = 32
    MAX = 2 ** ORDER
    g_mask = []
    for j in range(0, n):
        g_mask.append(2 ** j)
    g_mask.reverse()
    mask = 2 ** ORDER - 1
    W = 0
    P = 0
    h = [0]*n
    i = ORDER * n - n
    A = 0
    for j in range(0, n):
        if(pt[j] & mask):
            A |= g_mask[j]
    print A
    S = tS = A
    P = calc_P2(S, n, g_mask, MAX)
    element = i / ORDER
    if(i % ORDER > ORDER - n):
        h[element] |= (P * ( 2 ** i % ORDER)) % MAX
        h[element + 1] |= P / ( 2 ** ORDER - i % ORDER)
    else:
        h[element] |= (P * (2 ** i - element * ORDER)) % MAX
    
    J = calc_J(P, n)
    xJ = J - 1
    T = calc_T(P)
    tT = T

    mask /= 2
    i -= n
    while i >= 0:
        A = 0
        for j in range(0, n):
            if pt[j] & mask:
                A |= g_mask[j]
        W ^= tT
        tS = A ^ W
        S = calc_tS_tT(xJ, tS, n, MAX)
        P = calc_P2(S, n, g_mask, MAX)
        element = i / ORDER
        if i % ORDER > ORDER - n:
            h[element] |= (P * (2 ** i % ORDER)) % MAX
            h[element + 1] |= P / (2 ** ORDER - i % ORDER)
        else:
            h[element] |= (P * (2 ** i - element * ORDER)) % MAX
        if i > 0:
            T = calc_T(P)
            tT = calc_tS_tT(xJ, T, n, MAX)
            J = calc_J(P, n)
            xJ += J - 1
        print W    
        i -= n
        mask /= 2

    return h
        


# hilbert_key_decode
# point is an n dimensional pt, n is the dimensions, 
# and m is the order of the curve
"""
def hilbert_key_decode(point, n, m):
    mask = 2 ** ORDER - 1
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
