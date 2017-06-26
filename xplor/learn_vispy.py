"""this module is not usefull for the toolbox at all. It is simply a small
tutorial to understand how vispy works


using as a reference the following websites :
(2017 - 06)

(in French, 3D visualisation)
https://deptinfo-ensip.univ-poitiers.fr/ENS/doku/doku.php/stu:python_gui:vispy
"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#
# version 1.0
# -*- coding: utf-8 -*-


#  The system underlying the upcoming high-level visualization interfaces
from vispy import scene

# Application, event loops, canvas, backends
from vispy import app

# # User-friendly, Pythonic, object-oriented interface to OpenGL
# from vispy import gloo
#
# # OpenGL backend for matplotlib
# #from vispy import mpl_plot
#
# # Data IO
# from vispy import io
#
# #  Visualization-related geometry routines
# from vispy import geometry
#
# # Handling colors
# from vispy import color
#
# # Miscellaneous utilities
# from vispy import util
#
#
#
# # 1 /  create a canevas = a window
# # Creation of a canevas
# canvas = scene.SceneCanvas(title="Vis3D", size=(800, 600), keys='interactive',
#                            app='PyQt5')
#
# # Adding the view to the canevas (only one view for a canevas)
# view = canvas.central_widget.add_view()
#
# #
# # 2 / create an object to display
# #scene.visulals contains many objects such as :
# # Cube, Ellipse, GridLine, Image, Line, Mesh, Polygon, RegularPolygon
#
# #creation of a cube
# c = scene.visuals.Cube((1.0, 1.0, 1.0), color=(0,1,1,1), edge_color='red')
# view.add(c)
#
#
#
# #display the canevas
# canvas.show()
# #start the app
# app.run()

import vispy
vispy.test()