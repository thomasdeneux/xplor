"""tests module is a module to test the others

The modules that need to be tested are :
    - xdata (shape of the data itself)

This module uses :
        numpy
        unittest
        
        xdata

"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#          Thomas Deneux CNRS <thomas.deneux@unic.cnrs-gif.fr>
#
# version 1.0
# -*- coding: utf-8 -*-

import numpy
import unittest

import xdata


class MyTestCase(unittest.TestCase):
    def test_xdata_module_DimensionDescription_class(self):
        p = xdata.DimensionDescription('prices', 'numeric', 'euros')
        r = xdata.DimensionDescription('racetimes', 'numeric', 
                           ['s', 1, 'ms', 0.001, 'min', 60, 'hour', 3600] )
        f = xdata.DimensionDescription ('fruits', 'string')
    
        print("Tests for the class DimensionDescriptions (module xdata): \n")
        
        print("Test 1: attributes have the correct type")
        #test sur prices (p)
        self.assertTrue(isinstance(p.label, str))
        self.assertTrue(isinstance(p.dimensiontype, str))
        self.assertTrue(isinstance(p.unit, str))
        self.assertTrue(isinstance(p.allunits, list))
        self.assertTrue(isinstance(p.allunits[0], dict))
        self.assertTrue(isinstance(p.allunits[0]['unit'], str))
        self.assertTrue(isinstance(p.allunits[0]['value'], float))
        #test sur racetimes (r)
        self.assertTrue(isinstance(r.label, str))
        self.assertTrue(isinstance(r.dimensiontype, str))
        self.assertTrue(isinstance(r.unit, str))
        self.assertTrue(isinstance(r.allunits, list))
        self.assertTrue(isinstance(r.allunits[2], dict))
        self.assertTrue(isinstance(r.allunits[2]['unit'], str))
        self.assertTrue(isinstance(r.allunits[2]['value'], float))
        #test sur fruits (f)
        self.assertTrue(isinstance(f.label, str))
        self.assertTrue(isinstance(f.dimensiontype, str))
        self.assertTrue(f.unit is None)
        self.assertTrue(f.allunits is None)
        print("Test 2: attributes have the correct value")
        #test sur prices (p)
        self.assertEqual(p.label, 'prices')
        self.assertEqual(p.dimensiontype, 'numeric')
        self.assertEqual(p.unit, 'euros') 
        self.assertEqual(p.allunits, [{'unit': 'euros', 'value' : 1}])
        #test sur racetimes (r)
        self.assertEqual(r.label, 'racetimes')
        self.assertEqual(r.dimensiontype, 'numeric')
        self.assertEqual(r.unit, 's')
        self.assertEqual(r.allunits, [{'unit': 'ms', 'value': 0.001},
                                            {'unit': 's', 'value': 1.0},
                                            {'unit': 'min', 'value': 60.0},
                                            {'unit': 'hour', 'value': 3600.0}])
        #test sur fruits (f)
        self.assertEqual(f.label, 'fruits')
        self.assertEqual(f.dimensiontype, 'string')
        self.assertEqual(f.unit, None) 
        self.assertEqual(f.allunits, None)
        print("Test 3: raising errors for arguments with wrong types")
        #test sur prices (p)
        self.assertRaises(Exception, xdata.DimensionDescription, 1, 'numeric')
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices', 5)
        self.assertRaises(Exception, xdata.DimensionDescription, 'fruits',
                          'string', 'kg')
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', [])
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', ['s', 1, 'ms'])
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', [])
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', [1, 's', 0.001, 'ms'])
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', ['s', '1', 'ms', '0.001'])
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', ['s', 0.001, 'ms', 0.000001])
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', {'s' : 1})
        print("Test 4: function infertype")
        #no getdefaultvalue
        self.assertTrue(xdata.DimensionDescription.infertype(0), 'numeric')
        self.assertTrue(xdata.DimensionDescription.infertype(0.03), 'numeric')
        self.assertTrue(xdata.DimensionDescription.infertype('hahaha'),
                        'string')
        self.assertTrue(xdata.DimensionDescription.infertype([]), 'mixed')
        self.assertTrue(xdata.DimensionDescription.infertype(True), 'logical')
        self.assertTrue(xdata.DimensionDescription.infertype((1,12,200),
                                                            'color'))
        self.assertTrue(xdata.DimensionDescription.infertype((-1,12,200),
                                                            'mixed'))
        self.assertTrue(xdata.DimensionDescription.infertype((1,12,275),
                                                            'mixed'))
        #getdifaultvalue = False
        self.assertTrue(xdata.DimensionDescription.infertype(0, False),
                        'numeric')
        #getdefaultvalue = True
        self.assertTrue(xdata.DimensionDescription.infertype(0, True), 
                        ('numeric', 0))
        
        
        print("Test 5: function defaultvalue")
        self.assertEqual(xdata.DimensionDescription.defaultvalue('numeric'), 0)
        self.assertEqual(xdata.DimensionDescription.defaultvalue('logical'),
                         False)
        self.assertEqual(xdata.DimensionDescription.defaultvalue('string'), '')
        self.assertTrue(xdata.DimensionDescription.defaultvalue('mixed')
        is None)
        self.assertRaises(Exception, xdata.DimensionDescription.defaultvalue, 
        'prices')
        self.assertRaises(Exception, xdata.DimensionDescription, 2)
        
        print("\n")
        
        
        
#    def test_xdata_module_CategoricalHeader_class(self):
#        print("Tests for the class CategoricalHeader (module xdata):")
#        print("\n")
#        fruitprices = xdata.DimensionDescription('prices',
#                                                'numeric',
#                                                'euros/kg')
#        values = numpy.array([['apple', 0.5, 'red'],
#                          ['pear', 0.75, 'green' ],
#                          ['banana', 0.66, 'yellow'],
#                          ['strawberry', 0.89, 'red']])
#        print(type(values))
#        fruits = xdata.CategoricalHeader('fruits',
#                                         ['fruits', fruitprices, 'colors'],
#                                         4,
#                                         values)
#        print("Test 1: attributes have the correct type")
#        #test pour fruits
#        self.assertTrue(isinstance(fruits.label, str))
#        self.assertTrue(isinstance(fruits.column_descriptors, list))
#        self.assertTrue(isinstance(fruits.column_descriptors[0], 
#                                   xdata.DimensionDescriptor))
#        self.assertTrue(isinstance(fruits.n_elem, int))
#        self.assertTrue(isinstance(fruits.values, numpy.ndarray))
#        print("Test 2: attributes have the correct value")
#        print("Test 3: raising errors for arguments with wrong types")
#        print("\n")
#    
    def test_xdata_module_MeasureHeader_class(self):
        x = xdata.MeasureHeader('x', 1, 6, 0.5, 'mm')
        # TODO get unit from bank and also path when it fails to find a correspondence
        #y = xdata.MeasureHeader('y', 1, 0, 0.5, 'mm', True)
        time = xdata.DimensionDescription('time', 'numeric', 's') 
        t = xdata.MeasureHeader('time',
                                0.6,
                                100,
                                0.2,
                                column_descriptors = time)
        t2 = xdata.MeasureHeader('time',
                                0.6,
                                100,
                                0.2,
                                's')
        print("Tests for the class MeasureHeader (module xdata): \n")
        print("Test 1: attributes have the correct type")
        self.assertTrue(isinstance(x.label,str))
        self.assertTrue(isinstance(x.scale,float))
        self.assertTrue(isinstance(x.start,float))
        self.assertTrue(isinstance(x.n_elem,int))
        self.assertTrue(isinstance(x.column_descriptors,list))
        self.assertTrue(isinstance(x.column_descriptors[0],
                                   xdata.DimensionDescription))
        self.assertTrue(isinstance(t.column_descriptors,list))
        self.assertTrue(isinstance(t.column_descriptors[0],
                                   xdata.DimensionDescription))
        print("Test 2: attributes have the correct value")
        self.assertEqual(x.label, 'x')
        self.assertEqual(x.start, 1)
        self.assertEqual(x.scale, 0.5)
        self.assertEqual(x.n_elem, 6)
        self.assertEqual(x.column_descriptors[0].label, 'x')
        self.assertEqual(x.column_descriptors[0].unit, 'mm')
        self.assertEqual(x.column_descriptors[0].dimensiontype, 'numeric')
        
        self.assertEqual(t.label, 'time')
        self.assertEqual(t.start, 0.6)
        self.assertEqual(t.scale, 0.2)
        self.assertEqual(t.n_elem, 100)
        self.assertEqual(t.column_descriptors[0].label, 'time')
        self.assertEqual(t.column_descriptors[0].unit, 's')
        self.assertEqual(t.column_descriptors[0].dimensiontype, 'numeric')
        print("Test 3: raising errors for arguments with wrong types")
        self.assertRaises(Exception, xdata.MeasureHeader,
                          t, 0, 100, 0.2, column_descriptors = time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', '0', 100, 0.2, column_descriptors = time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', 0, '100', 0.2, column_descriptors = time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', 0, 100, '0.2', column_descriptors = time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', 0, 100, 0.2, column_descriptors = time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 100, 0.2, 's', column_descriptors = time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, column_descriptors = 'time')
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, 's', 'ms')
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, checkbank = True)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, 4)
        print("Test 4: testing the __eq__ function")
        self.assertTrue(t == t2)
        self.assertFalse(x == t)
        print("Test 5: testing the __ne__ function")
        self.assertTrue(x!= t)
        self.assertFalse(t!=t2)
        print("Test 6: testing the getncolumns function")
        self.assertEqual(x.getncolumns(), 1)
        print("Test 7: testing the getunits function")
        self.assertEqual(x.getunits(), ['mm'])
        self.assertEqual(t.getunits(), ['s'])
        print("Test 8: testing the getallunits function")
        self.assertEqual(x.getallunits(), [[{'unit' : 'mm', 'value' : 1.0}]])
        self.assertEqual(t.getallunits(), [[{'unit' : 's', 'value' : 1.0}]])
        print("Test 9: testing the iscategorical function")
        self.assertFalse(x.iscategorical)
        print("Test 10: testing the getvalue function")
        self.assertEqual(x.getvalue(0), 1)
        self.assertEqual(x.getvalue(3,1), 2.5)
        self.assertRaises(Exception, x.getvalue, 3, 2)
        self.assertRaises(Exception, x.getvalue, 3, -1)
        self.assertRaises(Exception, x.getvalue, 'something')
        self.assertRaises(Exception, x.getvalue, -10)
        self.assertRaises(Exception, x.getvalue, 10)
        print("Test 11: testing the get_itemname function")
        self.assertRaises(Exception, x.get_itemname, 'coffee')
        self.assertRaises(Exception, x.get_itemname, 10)
        self.assertRaises(Exception, x.get_itemname, -10)
        self.assertRaises(Exception, x.get_itemname, ['chocolate', 'milk'])
        self.assertRaises(Exception, x.get_itemname, [10])
        self.assertEqual(x.get_itemname(0), 1)
        self.assertEqual(x.get_itemname([0]), [1])
        self.assertEqual(x.get_itemname([]), [])
        self.assertEqual(x.get_itemname([0, 1, 3, 2]), [1, 1.5, 2.5, 2.0])
        print("Test 12: testing the update_measureheader function")
        self.assertRaises(Exception, x.update_measureheader, 'orange')
        self.assertRaises(Exception, x.update_measureheader, n_elem = 'apple')
        self.assertRaises(Exception, x.update_measureheader, scale = 'cherry')
        self.assertEquals(x.update_measureheader(2).label, x.label)
        self.assertEquals(x.update_measureheader(2).start, 2)
        self.assertEquals(x.update_measureheader(n_elem = 0).n_elem, 0)
        self.assertEquals(x.update_measureheader(scale = 4).scale, 4)
        self.assertEquals(x.update_measureheader(2, 0).scale, 0.5)
        print("Test 13: testing ismeasure, iscategoricalwithvalue, and "
              "isundifferentiated")
        self.assertTrue(x.ismeasure)
        self.assertFalse(x.iscategoricalwithvalues)
        self.assertFalse(x.isundifferentiated)

        print("\n")
        
#    def test_xdata_module_Xdata_class(self):
#        print("Tests for the class Xdata (module xdata):")
#        print("\n")
#        return ("bye")
#    
#    def test_xdata_module_createDimensionDescription_function(self):
#        print("Test for the createDimensionDescription function \
#        (module xdata) \n")
#        self.assertRaises(Exception, xdata.createDimensionDescription, 1)
#        self.assertRaises(Exception,
#                          xdata.createDimensionDescription,'fruits', 1)
#        self.assertRaises(Exception,
#                          xdata.createDimensionDescription,'fruits',
#                                                           numpy.arange(15))
#        c = xdata.createDimensionDescription('cars')
#        fruits = numpy.array([['apple'], ['pear'], ['banana']])
#        f = xdata.createDimensionDescription ('fruits', fruits)
#        #mix = numpy.array([[1], [2], ['Nan'], [1]])
#        #m = xdata.createDimensionDescription('mix', mix)
#        
#        cdd = xdata.DimensionDescription('cars', 'mixed')
#        fdd = xdata.DimensionDescription('fruits', 'string')
#        #mdd = xdata.DimensionDescription('mix', 'mixed')
#        
#        self.assertEqual(c.label, cdd.label)
#        self.assertEqual(c.dimensiontype, cdd.dimensiontype)
#        #self.assertEqual(m.label, mdd.label)
#        #self.assertEqual(m.dimensiontype, mdd.dimensiontype)
#        self.assertEqual(f.label, fdd.label)
#        self.assertEqual(f.dimensiontype, fdd.dimensiontype)
       
             
#if __name__ == "__main__":    
#    firsttest = MyTestCase()
#    firsttest.test_xdata_module_DimensionDescription_class()
#    #firsttest.test_xdata_module_CategoricalHeader_class()
#    firsttest.test_xdata_module_MeasureHeader_class()
##    firsttest.test_xdata_module_Xdata_class()
##    firsttest.test_xdata_module_createDimensionDescription_function()
#    