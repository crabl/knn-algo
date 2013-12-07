# Hilbert Curve Visualization Code
# Copyright (C) 2013 Christopher Rabl

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from hilbert_old import *
import random

def draw_graph_2d(points, path, file_name):
    plt.clf()
    fig = plt.figure()

    x = [v[0] for v in path]
    y = [v[1] for v in path]
    plt.plot(x,y, color='#FF0000', ls='-', alpha=0.45)

    point_x = [p[0] for p in points]
    point_y = [p[1] for p in points]
    plt.plot(point_x, point_y, marker='o', color='#BEF202', ls='')

    plt.axis([-1,16, -1, 16])

    fig.savefig(file_name, filetype="jpg")

def draw_graph_3d(points, path, file_name, el, az):
    plt.clf() # Clear the figure
    fig = plt.figure()
    plt.figure.max_num_figures = 20
    ax = Axes3D(fig)

    # Draw lines between codebook vectors
    x = [v[0] for v in path]
    y = [v[1] for v in path]
    z = [v[2] for v in path]
    ax.plot(x,y,z, color='#000000', ls='-', alpha=0.25)

    point_x = [p[0] for p in points]
    point_y = [p[1] for p in points]
    point_z = [p[2] for p in points]
    ax.plot(point_x, point_y, point_z, marker='o', color='#BEF202', ls='')

    ax.view_init(el, az)
    fig.savefig(file_name, filetype="jpg")

def random_2d_point():
    return (random.randint(0,15), random.randint(0,15))

def random_3d_point():
    return (random.randint(0,15), random.randint(0,15), random.randint(0,15))

def main():
    #points_16 = [(x,y,z) for x in range(16) for y in range(16) for z in range(16)]
    points_16 = [(x,y) for y in range(16) for x in range(16)]
    print "Performing Hilbert ordering..."
    data_set = [random_2d_point() for i in range(50)]
    hilbert_path = [hilbert_index(2,16,point) for point in points_16]
    ordered_path = [point for (h,point) in sorted(zip(hilbert_path, points_16))]
    #data_set = [random_3d_point() for i in range(20)]
    #data_set = [random_2d_point() for i in range(20)]
    print "Drawing graph..."

    for i in range(len(ordered_path)+1):
        #draw_graph_3d(data_set, ordered_path[0:i], "animation/hilbert"+str(i)+".jpg", 30, i % 360)
        draw_graph_2d(data_set, ordered_path[0:i], "animation/hilbert"+str(i)+".jpg")
    
if __name__ == "__main__":
    main()
