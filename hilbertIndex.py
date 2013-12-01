#!/usr/bin/env python
# Hilbert Keying Algo

#run source venv
import math
import bitstring

# gray code
def gc(i): 
    return i ^ (i >> 1)

# gray code Inverse
def gcInverse(g):
    if g == 0:
        return 0
    m = int(math.floor(math.log(g, 2))+1) # number of bits required to represent g
    i = g
    j = 1
    while j < m:
        i = i ^ (g >> j)
        j =  j + 1
    return i

# does a left bitwise rotation of a by b bits, with the number of bits in a 
#    being m
def leftRotate(a, b, m):
    w = bitstring.BitArray(uint = a, length = m)
    w.rol(b)
    return int(w.uint)

def rightRotate(a, b, m):
    w = bitstring.BitArray(uint = a, length = m)
    w.ror(b)
    return int(w.uint)

def g(i):
    return int(math.log(gc(i) ^ gc(i+1), 2))

def D(i, n):
    if i < 0:
        print "d: WHY IS THERE A NEGATIVE NUMBER >:|"
        return 0
    elif i == 0:
        return 0
    elif (i % 2) == 0:
        return g(i - 1) % n
    elif (i % 2) == 1:
        return g(i) % n
    else:
        print "d: FIX ME!!!!!!"
        return 0

def E(i, n):
    if i == 0:
        return 0
    return E(i - 1, n) ^ (2 ** D(i - 1, n)) ^ (2 ** g(i - 1))

"""
    if i < 0:
        print "e: THERE SHOULD NOT BE NEGATIVE NUMBERS >:|"
        return 0
    elif i == 0:
        return 0
    elif i <= 2 ** n - 1:
        return gc(int(2*math.floor(i - 1 / 2)))
    # I am not sure if this is what the paper means or not
    else:
        #print "e: YOU ARE BIGGER THAN 2 ** n - 1"
        return (gc(int(2*math.floor(i - 1 / 2)))) ^ (2 ** (n - 1))
"""


def L(i, p, n, m):
    l = bitstring.BitArray()
    for j in range(0, n):
        q = bitstring.BitArray(uint = p[j], length = m)
        q.reverse()
        l += q[i:i + 1]
    l.reverse()
    return int(l.uint)
        


# n is the number of dimensions
# m is the precision (# of bits) of each of the n dimensions
# p is the n dimensional point to convert into a hilbert index
def hilbertIndex(n, m, p):
    h = 0
    e = 0
    d = 0
    for q in range(1, m + 1):
        i = m - q
        l = L(i, p, n, m)# l <-[bit(p_(n-1),i)...bit(p_0, i)]_[2]u
        l = rightRotate((l ^ e), (d+1), m) # l <- T_(e, d) (l)
        w = gcInverse(l)
        e = e ^ (leftRotate(E(w, n), (d+1), m))
        d = (d + D(w, n) + 1) % n
        h = (h << n) | w
    return h
