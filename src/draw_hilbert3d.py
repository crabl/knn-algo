import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from hilbertIndex import *
import random

def draw_graph_2d(points, path, file_name):
    plt.clf()
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    x = [v[0] for v in path]
    y = [v[1] for v in path]
    ax.plot(x,y, color='#000000', ls='-', alpha=0.25)

    point_x = [p[0] for p in points]
    point_y = [p[1] for p in points]
    ax.plot(point_x, point_y, marker='o', color='#BEF202', ls='')

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
    return (random.randint(0,7), random.randint(0,7))

def random_3d_point():
    return (random.randint(0,7), random.randint(0,7), random.randint(0,7))

def main():
    points_8 = [(x,y,z) for x in range(8) for y in range(8) for z in range(8)]
    #points_8 = [(x,y) for y in range(8) for x in range(8)]
    print "Performing Hilbert ordering..."
    hilbert_path = [hilbertIndex(3,8,point) for point in points_8]
    ordered_path = [point for (hilbert_index,point) in sorted(zip(hilbert_path, points_8))]
    data_set = [random_3d_point() for i in range(20)]
    #data_set = [random_2d_point() for i in range(20)]
    print ordered_path
    print "Drawing graph..."

    for i in range(len(ordered_path)):
        draw_graph_3d(data_set, ordered_path[0:i], "animation/hilbert"+str(i)+".jpg", 30, i % 360)
        #draw_graph_2d(data_set, ordered_path[0:i], "animation/hilbert"+str(i)+".jpg")
    
if __name__ == "__main__":
    main()
