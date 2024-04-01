import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

filename = 'Coords.txt'
with open(filename, 'r') as file:
    lines = file.readlines()

x_coords = []
y_coords = []
z_coords = []
for line in lines:
    x, y, z = map(float, line.split())
    x_coords.append(x)
    y_coords.append(y)
    z_coords.append(z)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x_coords, y_coords, z_coords)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
