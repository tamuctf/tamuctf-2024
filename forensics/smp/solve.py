import importlib
import os
# importlib.import_module('mpl_toolkits').__path__
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import regex as re
from matplotlib import pyplot

# Define a function to parse the data and extract positions
def parse_data(filename):
    positions = []  # List to store tuples of positions
    with open(filename, 'r') as file:

        data = file.readlines()
        filelen = len(data)
        #    print(data)
        for i in range(filelen):
            line = data[i]
            #print(line)
            #print(line)
            if "Block Update" in line:
                #if("15," in data[i+2]):
                    try:
                        x = int(re.findall(r'-?\d+',data[i+4])[0])  # Extract x position
                        y = int(re.findall(r'-?\d+',data[i+5])[0])  # Extract y position
                        z = int(re.findall(r'-?\d+',data[i+6])[0])  # Extract z position
                        #print(x)
                        cords = (x,y,z)
                        positions.append(cords)
                    except:
                        pass
                #print(data)
                #y = int(data[10][:-1])  # Extract y position
                #z = int(data[12])  # Extract z position
                #positions.append((x, y, z))  # Insert the tuple into the list

    return positions
    
# Takes in a list of (x,y,z) tuples and plots them in a 3d graph 
def do_plotting(coords: list):
    #plt.autoscale(tight=True)
    # gridmap method



    # matplotlib method
    fig = plt.figure()

    ax = plt.axes(projection='3d')
    ax.axes.set_xlim3d(left=-200,right=200)
    ax.axes.set_zlim3d(bottom=-200,top=200)
    ax.axes.set_ylim3d(bottom=-200,top=200)
    x = []
    y = []
    z = []
    for coord in coords:
        x.append(coord[0])
        y.append(coord[1])
        z.append(coord[2])
    ax.scatter(x,y,z)
    ax.set_title('lmao minecraft map changes')
    plt.show()


#print(parse_data("./e"))
os.system("cat ./smp.log | grep \"Block Update\" -A 8  > parsed_file.txt")
do_plotting(parse_data("./parsed_file.txt"))


