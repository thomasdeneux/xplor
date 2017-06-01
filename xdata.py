"""xdata module is a module to define data in the form of an ND array

XPLOR dataset is contained in a N dimensional array. The array contains the 
data itself, but the array also has headers. The headers contains this
informations about each of the dimensions : names, types, units, scale, ...

This module uses : 
        numpy
        operator

There are 3 classes in this module:
    
    - Dimensionlabel : for a specific dimension, Dimensionlabel stores a label,
                        a dimensiontype ('numeric', 'logical', 'string', or 
                        'mixed'), possibly a unit and the corresponding
                        conversion table.
                        
                        It allows to determine the dimensiontype of an element,
                        and access the default value of a given dimensiontype.
                        
                        
    - Header
    - Xdata
"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#          Thomas Deneux CNRS <thomas.deneux@unic.cnrs-gif.fr>
#
# version 1.0
# -*- coding: utf-8 -*-

import numpy as np
from operator import itemgetter

class Dimensionlabel:
    
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
     dimensionlabel(label,type,unit)
    
     tlabel = dimensionlabel('time','numeric',['s, 1, 'ms', 10**(-3),
                                               'min', 60, 'hour', 3600])
     clabel = dimensionlabel('condition','string')
     
    """
    
    
    def __init__(self, 
                 label,
                 dimensiontype,
                 unit = None):
        """Constructor of the class Dimensionlabel"""
        
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
            raise Exception('only numeric dimensionlabels can have a unit')
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
            return (dimtype,Dimensionlabel.defaultvalue(dimtype))
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
        else:
            #'mixed' type
            return None
    
    
                
if __name__ == "__main__":
    print('Dimensionlabel')
    #Dimensionlabel(1,'numeric')
    raise Exception('label must be a string')
    

        
            
        
        
        
        