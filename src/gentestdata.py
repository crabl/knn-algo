import random

f = open("lattice_40x40_random.csv", "w")

points = [(random.randint(0,100),random.randint(0,100),random.randint(0,100)) for x in range(40) for y in range(40) for  z in range(40)]

for (x,y,z) in points:
    f.write(str(x)+"\t"+str(y)+"\t"+str(z)+"\n")

f.close()
