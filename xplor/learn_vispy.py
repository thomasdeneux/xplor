"""this module is not usefull for the toolbox at all. It is simply a small
tutorial to understand how vispy works
"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#
# version 1.0
# -*- coding: utf-8 -*-



#  The system underlying the upcoming high-level visualization interfaces
from vispy import scene

# Application, event loops, canvas, backends
from vispy import app

from vispy.io import load_data_file, read_png
import sys

import numpy as np


# Creation of a canvas
canvas = scene.SceneCanvas(keys='interactive', size=(1000, 600),
                           show=True, app='PyQt5')

# creating a grid to add widgets onto it
grid = canvas.central_widget.add_grid(margin=10, spacing=0, border_color='k')


# first element to display is the title
title = scene.Label("name of the xdata element (unit)", color='white')
title.height_max = 40
grid.add_widget(title, row=0, col=0, col_span=2)

# second element is the left axis
yaxis = scene.AxisWidget(orientation='left',
                         axis_label='MeasureHeader',
                         axis_font_size=12,
                         axis_label_margin=50,
                         tick_label_margin=5)
yaxis.width_max = 80
grid.add_widget(yaxis, row=1, col=0)

# third element is the bottom axis
xaxis = scene.AxisWidget(orientation='bottom',
                         axis_label='CateroricalHeader',
                         axis_font_size=12,
                         axis_label_margin=50)

xaxis.height_max = 80
grid.add_widget(xaxis, row=2, col=1)

# padding to add some space near the border and make sure the graph can be read
# entirely
right_padding = grid.add_widget(row=1, col=3, row_span=1)
#the higher the padding the more space between the element and the border of
# the canvas
right_padding.width_max = 80


# adding the view (with a white border)
view1 = grid.add_view(row=1, col=1, border_color='white')
view2 = grid.add_view(row=1, col=2, border_color='blue')
# get the data and plot it
data = np.random.normal(size=(1000, 2))
data[0] = -10, -10
data[1] = 10, -10
data[2] = 10, 10
data[3] = -10, 10
data[4] = -10, -10

plot = scene.Line(data, parent=view1.scene)

# load an image
img_data = read_png(load_data_file('mona_lisa/mona_lisa_sm.png'))
interpolation = 'nearest'

image = scene.visuals.Image(img_data, interpolation=interpolation,
                            parent=view2.scene, method='subdivide')


# add vertical lines
vert_line1 = scene.InfiniteLine(0.5, [1.0, 0.0, 1.0, 1.0],
                                parent=view1.scene)
vert_region2 = scene.LinearRegion([0.7, 1.2], [0.0, 1.0, 0.0, 0.5],
                                  vertical=True,
                                  parent=view1.scene)
# add horizontal lines
hor_line1 = scene.InfiniteLine(0.8, [1.0, 0.0, 0.0, 1.0], vertical=False,
                               parent=view1.scene)
hor_line2 = scene.InfiniteLine(-5.1, [1.0, 1.0, 0.0, 1.0], vertical=False,
                               parent=view2.scene)

# 'panzoom' allows to zoom in and out on the data with the mouse.
# the axis are not yet modified because the camera only concerns the view
# only what's in the square with the white border
# However, this is not exactely what we want because we want to zoom in
# directions separately
# 'turntable' allows to turn the graph (useful for 3D)
# it is possible to link the cameras with .link(view1.camera)

view1.camera = 'panzoom'
view2.camera = 'turntable'
# lets link an axis to the view. When we zoom in the view, it modifies the
# scale of the axis as well. This is what we want for MeasureHeaders
yaxis.link_view(view1)

#display the canevas
canvas.show()
#start the app
app.run()


