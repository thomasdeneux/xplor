"""view module is a module that generates the user interface.
For each simultaneous visualisation of the data, xplor creates an
instance of Window. Window has an interactive canvas to display the data but
also a slicer to reshape the data before it can be displayed.
There are two distinct zones of the canvas : a display section were the sliced
data is displayed and were the user can adjust the zoom and the position of
the labels, and a control section were the user can select the various filters
that will be applied on the data.


This module uses:
    - numpy as np
    - vispy

There are 2 classes in this module:

    - **Window**:
        This class creates the main window with the control section and the
        display section.

    - **ViewDisplay**:
        This class handles the display of the axis, labels, and graphs (and
        their position).

"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#          Thomas Deneux CNRS <thomas.deneux@unic.cnrs-gif.fr>
#
# version 1.0
# -*- coding: utf-8 -*-


from vispy import scene
from vispy import app

# creating the canvas of window
canvas = scene.SceneCanvas(title = "xplor your data",
                           size = (800, 600),
                           position = (500, 100),
                           show = True,
                           app = 'PyQt5',
                           resizable = True,
                           #later shared
                           always_on_top = True,
                           bgcolor = 'gray')
# display the canevas
canvas.show()

# creating the grid to place the elements
global_grid = canvas.central_widget.add_grid()

# visually separating the control from the display
w, h = canvas.size

control_zone = global_grid.add_widget(row=0, col=0)
control_zone.bgcolor = "#999999"

control_display = global_grid.add_widget(row=0, col=1)
control_display.bgcolor = "#efefef"

control_zone.width_min = w/6
control_zone.width_max = w/6

# display zone

display_grid = control_display.add_grid()

# adding a title
display_title = scene.Label("name of the xdata element", color="#0026b0")
display_title.height_max = 60
display_grid.add_widget(display_title, row=0, col=3)


display_note = scene.Label("Display:", color="black")
display_note.height_max = 60
display_grid.add_widget(display_note, row=0, col=0)


# ading the data axis
data_axis = scene.AxisWidget(orientation='left',
                             axis_label='unit of data',
                             axis_font_size=10,
                             axis_label_margin=30,
                             tick_label_margin=5,
                             text_color="black")
data_axis.width_max = 50
display_grid.add_widget(data_axis, row=3, col=5)

# adding labels
xy_label = scene.Label("xy label", color="#0026b0")
x_main_label = scene.Label("x main label", color="#0026b0")
x_sub_label = scene.Label("x sub_label", color="#0026b0")
y_main_label = scene.Label("y main label", color="#0026b0")
y_sub_label = scene.Label("y sub_label", color="#0026b0")

display_grid.add_widget(xy_label, row=1, col=3)
display_grid.add_widget(x_main_label, row=3, col=0)
display_grid.add_widget(x_sub_label, row=3, col=1)
display_grid.add_widget(y_main_label, row=6, col=3)
display_grid.add_widget(y_sub_label, row=5, col=3)

# add the axis for x and y
x_axis = scene.AxisWidget(orientation='left',
                             axis_label='x axis unit',
                             axis_font_size=10,
                             axis_label_margin=30,
                             tick_label_margin=5,
                             text_color="black")
x_axis.width_max = 50
display_grid.add_widget(x_axis, row=3, col=2)

y_axis = scene.AxisWidget(orientation='bottom',
                             axis_label='y axis unit',
                             axis_font_size=10,
                             axis_label_margin=30,
                             tick_label_margin=5,
                             text_color="black")
display_grid.add_widget(y_axis, row=4, col=3)

# adding zoom
x_zoom = display_grid.add_widget(row=3, col=4)
x_zoom.bgcolor = "black"
x_zoom.width_min = 20
x_zoom.width_max = 20

y_zoom = display_grid.add_widget(row=2, col=3)
y_zoom.bgcolor = "black"
y_zoom.height_min = 20
y_zoom.height_max = 20

# adding the widget to display all the graphs in a grid
viewzone = display_grid.add_widget(row=3, col=3)
viewzone.border_color = "blue"
viewzone.width_min = w/2
viewzone.width_max = w/2
viewzone.height_min = w/2
viewzone.height_max = w/2

# start the app
app.run()


class ViewDisplay:
    """
    Handling of the graphs (position, scale, axis, labels...)

    This class will be further developed to add new features such as the zoom,
    interactive labels and many more.

    **Parameters**

    - window:
        For each simultaneous visualisation of the data, xplor creates an
        instance of Window. The window has the information on what to display
        and will contain the new visualisation.


    **Attributes**
    - window:
        Each ViewDisplay is linked to a Window instance. The window gives the
        ViewDisplay instance the xdata element to display with the correct
        filters and the ViewDisplay instance computes how to display it on the
        window's canvas.
    -
    - view :
        The graph(s) or images of xdata to be displayed on the window's canvas.
    - axis :
        The axis lnked to the view (headers' information) matrices
    """
