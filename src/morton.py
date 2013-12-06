def less_msb(x, y):
    return x < y and x < (x ^ y)

def cmp_zorder(a, b):
    j = 0
    k = 0
    x = 0
    dim = len(a)
    for k in range(dim):
        y = a[k] ^ b[k]
        if less_msb(x, y):
            j = k
            x = y
    return a[j] - b[j]
