import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

# Setting style with plt.style directive
plt.style.use('classic')

# Create a 3d plot
fig = plt.figure()
ax = plt.axes(projection="3d")

# Create data for 3d data
zline = np.linspace(0, 15, 1000)
xline = np.sin(zline)
yline = np.cos(zline)
ax.plot3D(xline, yline, zline, 'gray')

# Plot 3d points and lines
zdata = 15 * np.random.random(100)
xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap="Greens")

# Show plot
plt.show()
