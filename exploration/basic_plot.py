import matplotlib.pyplot as plt
import numpy as np

# Setting style with plt.style directive
plt.style.use('classic')

# Data for use
x = np.linspace(0, 10, 100)

# Create grid of plots
fig, ax = plt.subplots(2)  # ax will be array of 2 axes objects

# Call plot() method on each axes object
ax[0].plot(x, np.sin(x))
ax[1].plot(x, np.cos(x))

# Running matplotlib from script
# call once when open plot
plt.show()
