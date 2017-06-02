"""tests module is a module to test the others

The modules that need to be tested are :
    - xdata (shape of the data itself)

This module uses :
        unittest
        
        xdata

"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#          Thomas Deneux CNRS <thomas.deneux@unic.cnrs-gif.fr>
#
# version 1.0
# -*- coding: utf-8 -*-

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
        
        
        
    def test_xdata_module_Header_class(self):
        print("Tests for the class Header (module xdata):")
        print("\n")
        return ("bye")
        
    def test_xdata_module_Xdata_class(self):
        print("Tests for the class Xdata (module xdata):")
        print("\n")
        return ("bye")
        
        
print("hi")       
if __name__ == "__main__":    
    print("hi")
    firsttest = MyTestCase()
    firsttest.test_xdata_module_DimensionDescription_class()
    firsttest.test_xdata_module_Header_class()
    firsttest.test_xdata_module_Xdata_class()
    