.. toctree::
   :maxdepth: 2
   :caption: Contents:


Structure
*********

.. image:: \images\GlobalDiagram.png
   :align: center
   :alt: UML diagram of all Xplor's modules

The module **xdata** aims at the creation of a container for the N dimensional
data and all the relative information on the dimensions and the data itself.

**view**'s main class is Window. Window creates the canvas (i.e. the window)
on witch to display the data. This canvas is composed of a control zone, where
the user can select the filters to apply, and a display zone, in which the user
can zoom and change the labels' position. Window also possesses a Slicer
instance and a ZoomSlicer instance to apply the correct filters on the Xdata
instance.

The module **operation** contains differents types of Filters as well as a
Slicer class and a ZoomSlicer class that will apply a succession of Filters on
the Xdata instance. The result of this operation is what is going to be
displayed on the canvas.

**Bank** is used to store previously used Headers and units, to save the user
some time.

TODO: explain other modules ?
      add some illustrations