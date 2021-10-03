import json
import os
from collections import defaultdict

import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as pp
import numpy as np
from matplotlib.font_manager import FontManager
from pylab import imread
from scipy.interpolate import Rbf

# Create file path to current source directory
source_path = os.path.expanduser(os.getenv('USERPROFILE')) + r"\Desktop\citrus"
coord_log_path = source_path + r"\workspace\log_2021-10-03.txt"
wifi_log_path = source_path + r"\workspace\2021-10-03.txt"

# Write parser to parse logs
store = []

with open(coord_log_path, "r") as f:
    for line in f:
        temp = {}
        tokenized = line.replace("\n", "").replace(" ", "").split("|")
        tokenized = [x.split(":")[1] for x in tokenized]

        # Do conversion from tkinter coordinate space to dxf coordinate space
        conv_x = tokenized[0]
        conv_y = tokenized[1]

        temp["x"] = conv_x
        temp["y"] = conv_y
        store.append(temp)

idx = 0
with open(wifi_log_path, "r") as f:
    for line in f:
        loaded = json.loads(line.replace("'", "\""))

        for key, value in loaded.items():
            store[idx][key] = value
        idx += 1

# Organize data into usable plotting form - each key organized into list
survey_points = defaultdict(list)
for item in store:
    for k, v in item.items():
        survey_points[k].append(item[k])

# Read in floorplan image
floorplan_filepath = source_path + r"\test.png"

floorplan = imread(floorplan_filepath)
floorplan_width = len(floorplan[0])
floorplan_height = len(floorplan) - 1
floorplan_corner_coord = [
    (0, 0), (0, floorplan_height),
    (floorplan_width, 0), (floorplan_width, floorplan_height)
]

for x, y in floorplan_corner_coord:
    survey_points['x'].append(x)
    survey_points['y'].append(y)
    for k in survey_points.keys():
        if k in ['x', 'y', 'ssid']:
            continue
        survey_points['ssid'].append(None)
        survey_points[k] = [0 if x is None else x for x in survey_points[k]]
        survey_points[k].append(min(survey_points[k]))

# Do plot
num_x = int(floorplan_width/4)
num_y = int(num_x/(floorplan_width/floorplan_height))
x = np.linspace(0, floorplan_width, num_x)
y = np.linspace(0, floorplan_height, num_y)
gx, gy = np.meshgrid(x, y)
gx, gy = gx.flatten(), gy.flatten()

# Set plot axis and title
pp.rcParams['figure.figsize'] = (
    floorplan_width / 300, floorplan_height / 300
)
fig, ax = pp.subplots()
title = "rssi"
ax.set_title(title)

# Fix plot threshold max and min
vmin = min(survey_points['rssi'])
vmax = max(survey_points['rssi'])

if vmin != vmax:
    rbf = Rbf(
        survey_points['x'], survey_points['y'], survey_points['rssi'], function='linear'
    )
    z = rbf(gx, gy)
    z = z.reshape((num_y, num_x))
else:
    # Uniform array with the same color everywhere
    # (avoids interpolation artifacts)
    z = np.ones((num_y, num_x))*vmin

# Render the interpolated data to the plot
ax.axis('off')

# Create color map for plot reference
cmap = pp.get_cmap()

# begin color mapping
norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax, clip=True)
mapper = cm.ScalarMappable(norm=norm, cmap=cmap)
# end color mapping
image = ax.imshow(
    z,
    extent=(0, floorplan_width, floorplan_height, 0),
    alpha=0.5, zorder=100,
    cmap=cmap, vmin=vmin, vmax=vmax
)

# Draw floorplan itself to the lowest layer with full opacity
ax.imshow(floorplan, interpolation='bicubic', zorder=1, alpha=1)
labelsize = FontManager.get_default_size() * 0.4

# Show points
# for idx in range(0, len(survey_points['tk_x'])):
#     if(survey_points['tk_x'][idx], survey_points['tk_y'][idx]) in floorplan_corner_coord:
#         continue

#     ax.plot(
#         survey_points['tk_x'][idx], survey_points['tk_y'][idx], zorder=200,
#         marker='o', markeredgecolor='black', markeredgewidth=1,
#         markerfacecolor=mapper.to_rgba(survey_points['rssi'][idx]), markersize=6
#     )
#     ax.text(
#         survey_points['tk_x'][idx], survey_points['tk_y'][idx] - 30,
#         survey_points['ssid'][idx], fontsize=labelsize,
#         horizontalalignment='center'
#     )
fname = f"rssi_{title}.png"
pp.savefig(fname, dpi=300)
pp.close('all')
