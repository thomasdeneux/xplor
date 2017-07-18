.. toctree::
   :maxdepth: 2
   :caption: Contents:


Module xdata : defining a data structure
****************************************

.. automodule:: xdata

**UML diagram of the  xdata module**

.. image:: \images\UML\module_xdata.png
   :align: center
   :alt: UML diagram for module xdata

Color class
-----------
.. autoclass:: Color

DimensionDescription class
--------------------------
.. autoclass:: DimensionDescription

Header abstract class
---------------------

**UML diagram of the abstract class Header and its subclasses**

.. image:: \images\UML\headers_simplified.png
   :align: center
   :alt: UML diagram for abstract class Header and subclasses

.. autoclass:: Header


CategoricalHeader  class
------------------------
.. autoclass:: CategoricalHeader


**Example of a CategoricalHeader with values**

         label: 'fruits'

         column_descriptors: (list of DimensionDescriptors, simplified here)
             1/ label: 'fruits', dimension_type: 'string', no unit

             2/ label: 'prices', dimension_type: 'numeric', unit: 'euros/kg'

             3/ label: 'color', dimension_type: 'string', no unit

         n_elem: 4

         values:
             [['apple', 0.5, 'red' ]

             ['pear', 0.75, 'green']

             ['banana', 0.66, 'yellow']

             ['cherry', 0.89, 'red']]


**Illustrations of the CategoricalHeader instance  (with values)**

.. image:: \images\examples_module_xdata\categoricalwithvalues.png
   :align: center
   :alt: illustration for a categorical header with values


**Example of an undifferentiated CategoricalHeader**

         label: 'fruits'

         column_descriptors (list of DimensionDescriptors): None

         n_elem: n

         values: None


**Illustrations of the CategoricalHeader instance  (undifferentiated)**

.. image:: \images\examples_module_xdata\undifferentiated.png
   :align: center
   :alt: illustration for an undifferentiated categorical header


MeasureHeader class
-------------------
.. autoclass:: MeasureHeader


**Example of a MeasureHeader**

        label: 't'

        column_descriptors: (list of one DimensionDescription)

            label: 't',

            dimension_type: 'numeric',

            unit: 'days',

            all_units:
            [{unit: 'hours', 'value': 1/24},
            {unit: 'days', 'value': 1},
            {unit: 'weeks', 'value': 7},
            {unit: 'months', 'value': 30.5}]

        n-elem: n

        start: 1

        scale: 0.25


**Illustrations of the MeasureHeader instance**

.. image:: \images\examples_module_xdata\measureheader.png
   :align: center
   :alt: illustration for a measure header

Xdata class
-----------

**UML diagram of the class Xdata**

.. image:: \images\UML\Xdata.png
   :align: center
   :alt: UML diagram for class Xdata

.. autoclass:: Xdata

**Example**

   Let's take the example of the growth of fruit trees.
   A gardener is interested in knowing how fast trees grow in the spring in
   a specific climate. He choses a few fruit trees to study, plants a few of
   each sort and watches them grow over time.

   In this example, we have 3 dimensions:
      - time called "t"
      - type of fruit tree simply called "fruits"
      - the fruit tree's number simply called "tree"

   Therefore, headers will be a list of the 3 headers given below.

   - "t" is a MeasureHeader:

         label: 't'

         column_descriptors: (list of one DimensionDescription)

            label: 't',

            dimension_type: 'numeric',

            unit: 'days',

            all_units:
            [{unit: 'hours', 'value': 1/24},
            {unit: 'days', 'value': 1},
            {unit: 'weeks', 'value': 7},
            {unit: 'months', 'value': 30.5}]

         n-elem: 100

         start: 0.5

         scale: 1

         **Illustrations of the MeasureHeader composing the Xdata instance**

         .. image:: \images\examples_module_xdata\measureheader.png
            :align: center
            :alt: illustration for a measure header
            :width: 80%

   - "tree" is a CategoricalHeader that is undifferentiated

         label: 'tree'

         column_descriptors (list of DimensionDescriptors): None

         n_elem: 8

         values: None


         **Illustrations of the undifferentiated CategoricalHeader of xdata**

         .. image:: \images\examples_module_xdata\undifferentiated.png
            :align: center
            :alt: illustration for a undifferentiated categorical header
            :width: 80%


   - "fruits" is a CategoricalHeader with values (because we can store some
      complementary information)

         label: 'fruits'

         column_descriptors: (list of DimensionDescriptors, simplified here)
             1/ label: 'fruits', dimension_type: 'string', no unit

             2/ label: 'prices', dimension_type: 'numeric', unit: 'euros/kg'

             3/ label: 'color', dimension_type: 'string', no unit

         n_elem: 4

         values:
             [['apple', 0.5, 'red' ]

             ['pear', 0.75, 'green']

             ['banana', 0.66, 'yellow']

             ['cherry', 0.89, 'red']]

         **Illustrations of the CategoricalHeader with values of xdata**

         .. image:: \images\examples_module_xdata\categoricalwithvalues.png
            :align: center
            :alt: illustration for a categorical header with values
            :width: 80%

   Now we have our list of headers, of length 3.


   The corresponding data is 3D array containing the values of the height
   of the tree at everyday for each of types of fruit trees. It is
   described (dimension_type and unit) the following data_descriptor:

         label: 'height', dimension_type: 'numeric', 'm'

   All we miss is the name of this set of data and headers: "Growth of
   the fruit trees in TreesCity"



   **Illustration of the Xdata instance**

   .. image:: \images\examples_module_xdata\xdataexample.png
      :align: center
      :alt: illustration for a xdata element


create_dimension_description function
-------------------------------------

.. autofunction:: xdata.create_dimension_description(label, column)

check_bank_unit function
------------------------

.. autofunction:: xdata.check_bank_unit(unit)