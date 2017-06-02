"""xdata module is a module to define data in the form of an ND array
XPLOR dataset is contained in a N dimensional array. The array contains the 
data itself, but the array also has headers. The headers contains this
informations about each of the dimensions : names, types, units, scale, ...
This module uses : 
        numpy
        operator
There are 3 classes in this module:
    
    - DimensionDescription : for a specific dimension, DimensionDescription 
                        stores a label,a dimensiontype ('numeric', 'logical',
                        'string', or 'mixed'), possibly a unit and the 
                        corresponding conversion table.
                        
                        It allows to determine the dimensiontype of an element,
                        and access the default value of a given dimensiontype.
                        
                        
    - Header
    - CategoricalHeader
    - MeasureHeader
    - Xdata
"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#          Thomas Deneux CNRS <thomas.deneux@unic.cnrs-gif.fr>
#
# version 1.0
# -*- coding: utf-8 -*-

import numpy as np
from operator import itemgetter
#this one is used to sort a list of dictionary
from abc import ABC, abstractmethod
#Header is abstract, subclasses are MeasureHeader and CategoricalHeader


class DimensionDescription:
    
    """ This class aims at defining a dimension.
    
    This class allows to define a dimension with a name, a type ('numeric,
    'logical', 'string' or 'mixed'), and possibly a unit for numerical 
    dimensions.
    
    Parameters
    ----------
    label : type : string (e.g. 'time')
            name for the dimension
    
     dimensiontype : values : 'numeric', 'logical', 'string' or 'mixed'
     
     unit : type : string or list, optional (default value = None)
            One can define only the unit (e.g. mm) or the conversions as well
            in the form of a list (e.g. ['mm', 10**(-3), 'm', 1])
     
     
    Attributes
    ----------
    label : name of the dimension
    dimensiontype : 'numeric', 'logical', 'string' or 'mixed'
    unit : currently used unit
    allunit : list for unit conversions
      
    Methods
    -------
    infertype (x, getdefaultvalue=False) : static
              gives the dimensiontype of the x element and possibly the
              associated defaultvalue
    defaultvalue (dimensiontype) : gives the default value associated to 
              a certain dimensiontype
    Examples
    --------
     DimensionDescription(label,type,unit)
    
     tlabel = DimensionDescription('time','numeric',['s, 1, 'ms', 10**(-3),
                                               'min', 60, 'hour', 3600])
     clabel = DimensionDescription('condition','string')
     
    """
    
    
    def __init__(self, 
                 label,
                 dimensiontype,
                 unit = None):
        """Constructor of the class DimensionDescription"""
        
        #Checking the arguments'types, raise an exception if it's not correct.
        #The label must be a string.
        if (not isinstance(label,str)):
            raise Exception('label must be a string')
        self._label = label
        #The dimensiontype must be 'numeric', 'logical', 'string, or 'mixed'.
        if not (dimensiontype in ['numeric', 'logical', 'string', 'mixed']):
            raise Exception("a dimensiontype must be 'numeric', 'logical', \
            'string' or 'mixed'")
        self._dimensiontype = dimensiontype
        #The unit is not compulsary (None for no unit).
        #However, only 'numeric' dimensions can have a unit.
        if (unit != None) & (dimensiontype != 'numeric'):
            raise Exception('only numeric DimensionDescriptions can have a \
            unit')
        #The unit can be given in the form of a string ...
        elif (isinstance(unit,str)):
            self._unit = unit
            self._allunits = [{'unit' : unit, 'value' : 1.0}]
        #..or in the form of a list of linked units and conversion coefficients
        elif unit==[]:
            raise Exception("there must be at least one unit")
        elif (isinstance(unit,list)):
            lengthlist = len(unit)
            if lengthlist%2 != 0:
                raise Exception("unit must be a string with the unit symbol or\
                 a list of the symbols of the unit followed by the conversion \
                indicator (e.g. ['mm', 10**(-3), 'm', 1]")
            #One of the units must be the reference.
            #That means that one conversion coefficient must be equal to one.
            Reference = False
            self._allunits = []
            for i in range (0,lengthlist,2):
                #The name of the unit is always a string.
                if not isinstance(unit[i],str):
                    raise Exception("unit names must be strings")
                #The coefficient for conversion must be int or float.
                if not (isinstance(unit[i+1],float)) | \
                       (isinstance(unit[i+1],int)):
                    raise Exception("conversion coeffs must be of type float \
                    or int")
                d = {'unit' : unit[i], 'value' : float(unit[i+1])}
                self._allunits += [d]
                if unit[i+1] == 1:
                    #A reference unit has been defined.
                    Reference = True
                    self._unit = unit[i]
            if not Reference:
                raise Exception("one of the conversion coefficients must be \
                equal to one to define a reference")
            #The list of units with conversion coefficients is sorted.
            self._allunits.sort(key=itemgetter('value'))
        #Checking if the type of unit is either str, list or if it is None.
        elif (unit != None):
            raise Exception("unit must be a string with the unit symbol or a \
            list  of the symbols of the unit followed by the conversion \
            indicator (e.g. ['mm', 10**(-3), 'm', 1]")
        else:
            self._unit = None
            self._allunits = None
                
                
    #Attributes label, dimensiontype, unit and allunits can be seen but not 
    #modified outside of the class (only get methods, no setters).
    @property
    def label(self):
        return self._label
    
    @property
    def dimensiontype(self):
        return self._dimensiontype
    
    @property
    def unit(self):
        return self._unit
    
    @property
    def allunits(self):
        return self._allunits
    
    #Determining the dimension type from some data.
    @staticmethod
    def infertype(x, getdefaultvalue=False):
        """infertype is a static method to access the dimensiontype of an
        element x and if required, the associated default value"""
        if isinstance(x,bool):
            dimtype = 'logical'
        elif isinstance(x,str):
            dimtype = 'string'
        elif type(x) in [int, float, complex]:
            dimtype = 'numeric'
        else:
            dimtype = 'mixed'
        
        if getdefaultvalue:
            return (dimtype,DimensionDescription.defaultvalue(dimtype))
        else:
            return dimtype
    
    #Calculating a default value for the differents dimensiontypes.
    @staticmethod
    def defaultvalue(dimensiontype):
        """defaultvalue is a static method to access the default value of a
        given dimensiontype"""
        if dimensiontype == 'numeric':
            return 0
        elif dimensiontype == 'logical':
            return False
        elif dimensiontype == 'string':
            return ''
        elif dimensiontype == 'mixed':
            return None
        else:
            raise Exception("This function only gives the default value for \
            the following types: 'numeric', 'logical', 'string', 'mixed'")






    
class Header(ABC):
    """ This abstract class allows the creation of headers for the different 
    dimensions of a dataset.
    
    Header is an abstract class that has two subclasses: CategoricalHeader and
    MeasureHeader.
    A Header object fully describes a dimension.
    A CategoricalHeader is used for data with  no regular organisation.
    It usually correspond to a list of elements. However,  such elements can
    have interesting features of different types. That's why such features are 
    stored in columns, each of them described by a DimensionDescriptor object.
    A MeasureHeader is used for data aquired by equally spaced sample in a
    continous dimension such as time or space. In wich case, their is only one
    subdimension (i.e. only one column).
    
    
    Parameters
    ----------     
     
    Attributes
    ----------
    - label : name of the dimension
    - columns_descriptor : list of the DimensionDescription of each of the 
    columns of values
    - n_elem : number of element in the column(s)/ number of samples
    - values : in the case of CategoricalHeader, values in the features of
    interest
    - start : for MeasureHeader, starting point of the sample (float)
    - scale : space between sample for MeasureHeader
    - id_header : unique id (calculated with a hashset), stored, to save
    calculation time when comparing two headers
      
    Methods
    -------
    
    Examples
    --------
     CategorialHeader:
         label : 
    
     TODO
     
    """
    #Attributes label, column_descriptor, lengthofvalues, values, start, scale 
    #and idheader can be seen but not modified outside of the class (only get 
    #methods, no setters).
    @property
    def label(self):
        return self._label
    
    @property
    def columns_descriptor(self):
        return self._columns_descriptor
    
    @property
    def n_elem(self):
        return self._n_elem
    
    @property
    def values(self):
        return self._values
    
    @property
    def start(self):
        return self._start
    
    @property
    def scale(self):
        return self._scale
    
    @property
    def id_header(self):
        return self._id_header
    
    
    
    @abstractmethod
    def disp(self):
        pass


class CategoricalHeader(Header):
    """ This class allows the creation of a header for a categorical dimensions
    of a dataset.
    
    CategoricalHeader is used for categorical dimensions of a dataset. This
    means that this dimension is either not continuous or that the data has not
    been collected regularly in this dimension. Therefore, their is no scale,
    measure for this dimension. It is more a collection of objects.
    
    A CategoricalHeader has a general label as well as one or several
    DimensionDescription objects stored in columns_descriptors to describe each
    of the features. For each feature, values can be given (e.g. for 'fruits'
    values would be 'apple', 'pear', 'blueberry', 'watermelon'...) or be a list
    of numbers. 
    
    
    Parameters
    ----------     
    - label: (otional if there is a columns_descriptor)
            type : str
            name of the header
            (if not specified, the label of the first element of
            columns_descriptor is used as the header's label)
    - columns_descriptor : (optional if there is a label)
            type : str, DimensionDescription or a list of such elements
            description of the dimension of each feature
    - n_elem : (optional if values is specified)
            type : int
            number of element in the column(s)
    - values : (otional if it is just an enumeration and that n_elem is given)
            type : numpy.array of shape (n_elem, len(columns_constructor))
            content of the various subdimensions
    
    Attributes
    ----------
    - label : name of the dimension (str)
    - columns_descriptor : list of the DimensionDescription of each of the 
            columns of values
    - n_elem : number of element in the column(s)
    - values : content of the various subdimensions (numpy.array of shape
            (n_elem, len(columns_constructor))
    - start : None
    - scale : None
    - id_header : unique id (calculated with a hashset), stored, to save
            calculation time when comparing two headers
      
    Methods
    -------
    TODO
    Examples
    --------
     CategorialHeader:
         label : 
    
     TODO
     
    """
    
    def __init__(self,
                 label = None,
                 columns_descriptor = None,
                 n_elem = None,
                 values = None):
        """Constructor of the class DimensionDescription"""
        
        #an empty array of values is considered as None
        if values == np.array(None):
            values = None
        elif (not isinstance(values, numpy.ndarray)) & (not values is None):
            raise Exception("values must be of type numpy.ndarray")
        #if no label is specified, create it from the columns_descriptor
        create_a_label = False
        if (isinstance(label,str)):
            self._label = label
        elif not (label is None):
            raise Exception("The header's label must be of type str")
        else:
            create_a_label = True
            if columns_descriptor is None:
                raise Exception("The header must have at least a label or a \
                columns_descriptor" )
        #columns_descriptors can be DimensionDescription or str (a single 
        #element or a list)
        #if no columns_descriptor is specified, create it from the label
        if (columns_descriptor is None) | (columns_descriptor == []):
            self._columns_descriptor = [createDimensionDescription(label,
                                                                  values)]
        elif isinstance(columns_descriptor, str):
            self._columns_descriptor = \
            [createDimensionDescription(columns_descriptor, values)]     
        elif isinstance(columns_descriptor, DimensionDescription):
            self._columns_descriptor = [columns_descriptor]
        elif not isinstance(columns_descriptor, list):
            raise Exception("columns_descriptor must be a single element or a \
            list of elements of type str or DimensionDescription")
        else:
            n_col = len(columns_descriptor)
            self._columns_descriptor = []
            if isinstance(values, numpy.ndarray) & \
                         values.shape[1] == n_col:
                for i in range (n_col):
                    if isinstance(columns_descriptor[i], str):
                        self._columns_descriptor += \
                        createDimensionDescription(columns_descriptor[i],
                                                   values[i])
                    elif isinstance(columns_descriptor[i],
                                    DimensionDescription):
                        self._columns_descriptor += columns_descriptor[i]
                    else:
                        raise Exception("all columns-descriptor elements must \
                        be either of type str or DimensionDescription)
            else:
                for i in range (n_col):
                    if isinstance(columns_descriptor[i], str):
                        self._columns_descriptor += \
                        createDimensionDescription(columns_descriptor[i])
                    elif isinstance(columns_descriptor[i],
                                    DimensionDescription):
                        self._columns_descriptor += columns_descriptor[i]
                    else:
                        raise Exception("all columns-descriptor elements must \
                        be either of type str or DimensionDescription)
        #adding a label to the header if none were given
        if create_a_label:
            self._label = self.columns_descriptor[0].label
        #if both values and n_elem were given, it must be coherent
        if n_elem is None:
            if isinstance(values, numpy.ndarray):
                self._n_elem = values.shape[0]
            else:
                raise Exception("either n_elem or values must be specified")
        elif not isinstance(n_elem, int):
            raise("n_elem must be of type int")
        elif isinstance(values, numpy.ndarray) & \
                   values.shape[0] == n_elem:
            self._n_elem = n_elem
        elif isinstance(values, numpy.ndarray) & \
                   values.shape[0] != n_elem:
            raise Execption("the number of lines of the values must be the \
            same as n_elem")
        else:
            self._n_elem = n_elem
        #the size of value must be checked
        if isinstance(values, numpy.ndarray) & \
                   values.shape[0] == self._n_elem & \
                   values.shape[1] == len(self._columns_descriptor):
                       self._values = values
        elif values is None:
            self._values = None
        else:
            raise Exception("values must be of type numpy.array")
                                   
         
                
            
