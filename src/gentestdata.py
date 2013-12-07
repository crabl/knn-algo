f = open("lattice_40x40.csv", "w")

points = [(x,y) for x in range(40) for y in range(40)]

for (x,y) in points:
    f.write(str(x)+"\t"+str(y)+"\n")

f.close()
