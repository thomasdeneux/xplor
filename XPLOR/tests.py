"""tests module is a module to test the others

The modules that need to be tested are :
    - xdata (shape of the data itself)

This module uses :
        numpy
        pandas
        unittest
        
        xdata

"""

# Authors: Elodie Ikkache CNRS <elodie.ikkache@student.ecp.fr>
#          Thomas Deneux CNRS <thomas.deneux@unic.cnrs-gif.fr>
#
# version 1.0
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
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
        print("Test 4: method infertype")
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

        print("Test 5: method defaultvalue")
        self.assertEqual(xdata.DimensionDescription.defaultvalue('numeric'), 0)
        self.assertEqual(xdata.DimensionDescription.defaultvalue('logical'),
                         False)
        self.assertEqual(xdata.DimensionDescription.defaultvalue('string'), '')
        self.assertTrue(xdata.DimensionDescription.defaultvalue('mixed')
        is None)
        self.assertRaises(Exception, xdata.DimensionDescription.defaultvalue, 
        'prices')
        self.assertRaises(Exception, xdata.DimensionDescription, 2)
        print ("Test 6 : method set_dimtype_to_mixed")
        f.set_dimtype_to_mixed()
        self.assertEqual(f.dimensiontype, 'mixed')
        print("Test 7: method copy")
        pcopy = p.copy()
        rcopy = r.copy()
        fcopy = f.copy()
        self.assertEqual(pcopy.allunits, [{'unit': 'euros', 'value' : 1}])
        self.assertEqual(rcopy.allunits, [{'unit': 'ms', 'value': 0.001},
                                          {'unit': 's', 'value': 1.0},
                                          {'unit': 'min', 'value': 60.0},
                                          {'unit': 'hour', 'value': 3600.0}])
        self.assertTrue(fcopy.allunits is None)
        print("\n")
        
        
        
    def test_xdata_module_CategoricalHeader_class(self):
        print("Tests for the class CategoricalHeader (module xdata):")
        print("\n")
        dfvalues = pd.DataFrame([['apple', 0.5, 'red'],
                                 ['pear', 0.75, 'green'],
                                 ['banana', 0.66, 'yellow'],
                                 ['cherry', 0.89, 'red']])
        fruits = xdata.CategoricalHeader('fruits',
                                         ['fruits', 'fruitprices', 'colors'],
                                         4,
                                         dfvalues)
        fruits3 = xdata.CategoricalHeader('fruits',
                                         ['fruits', 'fruitprices', 'colors'],
                                         4,
                                         dfvalues)
        fruitprices = xdata.DimensionDescription('prices',
                                                'numeric',
                                                'euros/kg')
        fruits2 = xdata.CategoricalHeader('fruits',
                                          ['fruits', fruitprices, 'colors'],
                                          values = dfvalues)
        undifferentiated = xdata.CategoricalHeader('repetitions', n_elem = 10)

        print("Test 1: attributes have the correct type")
        #tests for fruits
        self.assertTrue(isinstance(fruits.label, str))
        self.assertTrue(isinstance(fruits.column_descriptors, list))
        self.assertTrue(isinstance(fruits.column_descriptors[0], 
                                   xdata.DimensionDescription))
        self.assertTrue(isinstance(fruits.n_elem, int))
        self.assertTrue(isinstance(fruits.values,pd.core.frame.DataFrame))
        #tests for fruits2
        self.assertTrue(isinstance(fruits2.label, str))
        self.assertTrue(isinstance(fruits2.column_descriptors, list))
        self.assertTrue(isinstance(fruits2.column_descriptors[0], 
                                   xdata.DimensionDescription))
        self.assertTrue(isinstance(fruits2.n_elem, int))
        self.assertTrue(isinstance(fruits2.values,pd.core.frame.DataFrame))
        #tests for undifferentiated
        self.assertTrue(isinstance(undifferentiated.label, str))
        self.assertTrue(undifferentiated.column_descriptors is None)
        self.assertTrue(isinstance(undifferentiated.n_elem, int))
        self.assertTrue(isinstance(undifferentiated.values,
                                   pd.core.frame.DataFrame))
        print("Test 2: attributes have the correct value")
        #tests for fruits
        self.assertEqual(fruits.label, 'fruits')
        self.assertEqual(fruits.column_descriptors[0].label,
                         xdata.DimensionDescription('fruits', 'string').label)
        self.assertEqual(fruits.column_descriptors[0].dimensiontype,
                         xdata.DimensionDescription('fruits',
                                                    'string').dimensiontype)
        self.assertEqual(fruits.column_descriptors[1].label, 
                         xdata.DimensionDescription('fruitprices',
                                                    'numeric').label)
        self.assertEqual(fruits.column_descriptors[1].dimensiontype, 
                         xdata.DimensionDescription('fruitprices',
                                                    'numeric').dimensiontype)
        self.assertEqual(fruits.column_descriptors[2].label, 
                         xdata.DimensionDescription('colors',
                                                    'string').label)
        self.assertEqual(fruits.column_descriptors[2].dimensiontype, 
                         xdata.DimensionDescription('colors',
                                                    'string').dimensiontype)
        self.assertEqual(fruits.n_elem, 4)
        self.assertEqual(fruits.values[0][0], 'apple')
        self.assertEqual(fruits.values[1][0], 0.5)
        self.assertEqual(fruits.values[2][3], 'red')
        #tests for fruits2
        self.assertEqual(fruits2.label, 'fruits')
        self.assertEqual(fruits2.column_descriptors[0].label,
                         xdata.DimensionDescription('fruits','string').label)
        self.assertEqual(fruits2.column_descriptors[0].dimensiontype,
                         xdata.DimensionDescription('fruits',
                                                    'string').dimensiontype)
        self.assertEqual(fruits2.column_descriptors[1].label, 
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').label)
        self.assertEqual(fruits2.column_descriptors[1].dimensiontype, 
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').dimensiontype)
        self.assertEqual(fruits2.column_descriptors[1].unit, 
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').unit)
        self.assertEqual(fruits2.column_descriptors[1].allunits, 
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').allunits)
        self.assertEqual(fruits2.column_descriptors[2].label, 
                         xdata.DimensionDescription('colors',
                                                    'string').label)
        self.assertEqual(fruits2.column_descriptors[2].dimensiontype, 
                         xdata.DimensionDescription('colors',
                                                    'string').dimensiontype)
        self.assertEqual(fruits2.n_elem, 4)
        self.assertEqual(fruits2.values[0][0], 'apple')
        self.assertEqual(fruits2.values[1][0], 0.5)
        self.assertEqual(fruits2.values[2][3], 'red')        
        #tests for undifferentiated
        self.assertEqual(undifferentiated.label, 'repetitions')
        self.assertEqual(undifferentiated.n_elem, 10)
        self.assertEqual(undifferentiated.values.shape, (10,0))
        print("Test 3: raising errors for arguments with wrong types")
        self.assertRaises(Exception, xdata.CategoricalHeader, 1)
        self.assertRaises(Exception, xdata.CategoricalHeader, 'label')
        self.assertRaises(Exception,
                          xdata.CategoricalHeader, 'label', n_elem = 'n_elem')
        self.assertRaises(Exception,
                          xdata.CategoricalHeader, 'label', n_elem = 1,
                          column_descriptors = ['str'])
        self.assertRaises(Exception,
                          xdata.CategoricalHeader, 'label', values = [1, 2, 3])
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem = 1,
                          values = dfvalues)
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem = 'n_elem',
                          values = dfvalues)
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem = 1,
                          values = dfvalues,
                          column_descriptors = [])
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem = 1,
                          values = dfvalues,
                          column_descriptors = 56)
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem = 1,
                          values = dfvalues,
                          column_descriptors = ['fruits', 45])
        print("Test 4: testing the __eq__ method")
        self.assertTrue(fruits == fruits3)
        self.assertFalse(fruits == fruits2)
        print("Test 5: testing the __ne__ method")
        self.assertTrue(fruits!= fruits2)
        self.assertFalse(fruits!=fruits3)
        print("Test 6: testing the getncolumns method")
        self.assertEqual(fruits.getncolumns(), 3)
        self.assertEqual(undifferentiated.getncolumns(), 0)
        print("Test 7: testing the getunits method")
        self.assertEqual(undifferentiated.getunits(), [])
        self.assertEqual(fruits.getunits(), ['no unit', 'no unit', 'no unit'])
        self.assertEqual(fruits2.getunits(),
                         ['no unit', 'euros/kg', 'no unit'])
        print("Test 8: testing the getallunits method")
        self.assertEqual(undifferentiated.getallunits(), [])
        self.assertEqual(fruits.getallunits(), ['no unit', 'no unit', 'no unit'])
        self.assertEqual(fruits2.getallunits(),
                         ['no unit',
                          [{'unit' : 'euros/kg', 'value' : 1}],
                          'no unit'])
        print("Test 9: testing the iscategorical, ismeasure, "
              "iscategoricalwithvalue, and isundifferentiated")
        self.assertTrue(fruits.iscategorical)
        self.assertTrue(undifferentiated.iscategorical)
        self.assertFalse(fruits.ismeasure)
        self.assertFalse(undifferentiated.ismeasure)
        self.assertTrue(fruits.iscategoricalwithvalues)
        self.assertFalse(undifferentiated.iscategoricalwithvalues)
        self.assertFalse(fruits.isundifferentiated)
        self.assertTrue(undifferentiated.isundifferentiated)
        print("Test 10: testing the getvalue method")
        self.assertEqual(undifferentiated.getvalue(0), 0)
        self.assertEqual(fruits.getvalue(2,1), 0.66)
        self.assertEqual(fruits.getvalue(2), 'banana')
        self.assertEqual(fruits.getvalue(2, 'fruits'), 'banana')
        self.assertRaises(Exception, fruits.getvalue, '2')
        self.assertRaises(Exception, fruits.getvalue, -3)
        self.assertRaises(Exception, fruits.getvalue, 10)
        print("Test 11: testing the get_itemname method")
        self.assertRaises(Exception, fruits.get_itemname, 'coffee')
        self.assertRaises(Exception, fruits.get_itemname, 10)
        self.assertRaises(Exception, fruits.get_itemname, -10)
        self.assertRaises(Exception, fruits.get_itemname, ['chocolate', 'milk'])
        self.assertRaises(Exception, fruits.get_itemname, [10])
        self.assertEqual(fruits.get_itemname(0), 'apple')
        self.assertEqual(fruits.get_itemname([0]), ['apple'])
        self.assertEqual(fruits.get_itemname([]), [])
        self.assertEqual(fruits.get_itemname([0, 1, 3, 2]),
                                             ['apple',
                                             'pear',
                                             'cherry',
                                             'banana'])
        print("Test 12: testing the update_measureheader method")
        wrongsizecol = pd.DataFrame([['apple', 0.5, 'red', 'yummy'],
                                     ['pear', 0.75, 'green', 'yummy'],
                                     ['banana', 0.66, 'yellow', 'yummy'],
                                     ['cherry', 0.89, 'red', 'yummy']])
        wrongdimtype = pd.DataFrame([['apple', '0.5', 'red'],
                                     ['pear', 0.75, 'green'],
                                     ['banana', 0.66, 'yellow'],
                                     ['cherry', 0.89, 'red']])
        #testing for flag 'all'
        allfruits = fruits.update_categoricalheader('all', None, wrongdimtype)
        self.assertEqual(allfruits.label, fruits.label)
        self.assertEqual(allfruits.column_descriptors[1].dimensiontype,
                         'mixed')
        self.assertEqual(allfruits.values.shape, (4,3))
        self.assertRaises(Exception,
                          fruits.update_categoricalheader,
                          'all',
                          [2, 4],
                          dfvalues)
        self.assertRaises(Exception,
                          fruits.update_categoricalheader,
                          'all',
                          None,
                          [1, 2, 3])
        self.assertRaises(Exception,
                          fruits.update_categoricalheader,
                          'all',
                          None,
                          wrongsizecol)
        #testing for flag 'new'
        series = [pd.Series(['kiwi', 0.95, 'brown']), 
                  pd.Series(['blueberry', '1.20', 'blue'])]
        newfruits = fruits.update_categoricalheader('new', None, series)
        self.assertEqual(newfruits.label, fruits.label)
        self.assertEqual(newfruits.column_descriptors[1].dimensiontype,
                         'mixed')
        self.assertEqual(newfruits.values.shape, (6, 3))
        self.assertEqual(newfruits.values[1][5], '1.20')
        self.assertEqual(newfruits.values[0][4], 'kiwi')
        self.assertEqual(newfruits.values[1][4], 0.95)
        self.assertRaises(Exception,
                          fruits.update_categoricalheader,
                          'new', 1, series)
        self.assertRaises(Exception,
                          fruits.update_categoricalheader,
                          'new', [], pd.Series(['kiwi', 0.95, 'brown']))
        self.assertRaises(Exception,
                          fruits.update_categoricalheader,
                          'new', [], [1, 2])
        self.assertRaises(Exception,
                          fruits.update_categoricalheader,
                          'new',
                          [],
                          [pd.Series(['kiwi', 0.95, 'brown', 'yummy']), 
                           pd.Series(['blueberry', '1.20', 'blue', 'yummy'])])
        #testing for flag 'chg'
        chgfruits = fruits.update_categoricalheader('chg', [1, 3], series)
        self.assertEqual(chgfruits.label, fruits.label)
        self.assertEqual(chgfruits.column_descriptors[1].dimensiontype,
                         'mixed')
        self.assertEqual(chgfruits.values.shape, (4, 3))
        self.assertEqual(chgfruits.values[1][3], '1.20')
        self.assertEqual(chgfruits.values[0][1], 'kiwi')
        self.assertEqual(chgfruits.values[1][1], 0.95)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg', 1, series)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg', [1], 'yummy')
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg', [1, -3], series)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg', [122, 1], series)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg', ['14', 1], series)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg', [1], ['yummy'])
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg', [1, 2],
                          [pd.Series(['kiwi', 0.95, 'brown', 'yummy']), 
                           pd.Series(['blueberry', '1.20', 'blue', 'yummy'])])
        #testing for flag 'remove'
        removefruits = fruits.update_categoricalheader('remove', [2], [])
        self.assertEqual(removefruits.label, fruits.label)
        self.assertEqual(removefruits.values.shape, (3, 3))
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'remove', 1, None)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'remove', [12], None)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'remove', [-1], None)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'remove', ['yummy'], None)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'remove', [1], [1])
        #testing for flag 'perm'
        permfruits = fruits.update_categoricalheader('perm',
                                                     [1, 2, 3, 0],
                                                     None)
        self.assertEqual(permfruits.label, fruits.label)
        self.assertEqual(permfruits.values[0][1], fruits.values[0][2])
        self.assertEqual(permfruits.values[1][3], fruits.values[1][0])
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'perm', [1, 2, 3, 0], [1])
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'perm', 'yummy', None)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'perm', [1, 2], None)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'perm', ['yummy', 2, 3, 0], None)
        #testing for flag 'chg&new'
        chgandnewfruits1 = fruits.update_categoricalheader('chg&new',
                                                     [1, 2],
                                                     [series, series])
        chgandnewfruits2 = fruits.update_categoricalheader('chg&new',
                                                     [[3, 2], []],
                                                     [series, series])
        self.assertEquals(chgandnewfruits1.label,
                          fruits.label,
                          chgandnewfruits2.label)
        self.assertEquals(len(chgandnewfruits1.column_descriptors),
                          len(fruits.column_descriptors),
                          len(chgandnewfruits2.column_descriptors))
        self.assertEquals(chgandnewfruits1.values.shape,
                          chgandnewfruits2.values.shape,
                          (6, 3))
        self.assertEqual(chgandnewfruits1.values[0][1], 'kiwi')
        self.assertEqual(chgandnewfruits1.values[0][2], 'blueberry')
        self.assertEqual(chgandnewfruits1.values[0][4], 'kiwi')
        self.assertEqual(chgandnewfruits1.values[0][5], 'blueberry')
        self.assertEqual(chgandnewfruits2.values[0][3], 'kiwi')
        self.assertEqual(chgandnewfruits2.values[0][2], 'blueberry')
        self.assertEqual(chgandnewfruits2.values[0][4], 'kiwi')
        self.assertEqual(chgandnewfruits2.values[0][5], 'blueberry')
        self.assertEquals(chgandnewfruits1.column_descriptors[1].dimensiontype,
                          chgandnewfruits2.column_descriptors[1].dimensiontype,
                          'mixed')
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg&new', 1, [series, series])
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg&new', [1,2], 'yummy')
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg&new', [1,2], series)
        #testing for flag 'chg&rm'
        chgandrmfruits = fruits.update_categoricalheader('chg&rm',
                                                     [[1, 2], [0]],
                                                     series)
        self.assertEqual(chgandrmfruits.label, fruits.label)
        self.assertEqual(chgandrmfruits.getncolumns(), fruits.getncolumns())
        self.assertEqual(chgandrmfruits.values.shape, (3,3))
        self.assertEqual(chgandrmfruits.values[0][0], 'kiwi')
        self.assertEqual(chgandrmfruits.values[0][1], 'blueberry')
        self.assertEqual(chgandrmfruits.values[0][2], 'cherry')
        self.assertEquals(chgandrmfruits.column_descriptors[1].dimensiontype,
                          'mixed')
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg&rm', 1, series)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg&rm', [1, 2, 3], series)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg&rm', [1, 2], series)
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chg&rm', [[1,2], []], 'yummy')
        #testing for not a flag or a flag that is not accepted by the method
        self.assertRaises(Exception, fruits.update_categoricalheader,
                          'chgdim', [], [])
        print("Test 13: testing check_header_update method")
        #this method is a test itself, it does not return anything, it only
        #raises exceptions when there is an obvious problem (not a good name,
        #not a good size)
        #We conduct a few tests on this testing methods, but the method is not
        #fully covered
        self.assertRaises(Exception, fruits.check_header_update,
                          'yummy', np.array([1]), chgandrmfruits)
        self.assertRaises(Exception, fruits.check_header_update,
                          'new', [], chgandrmfruits)
        self.assertRaises(Exception, fruits.check_header_update,
                          'new', np.array([1]), 'yummy')
        t2 = xdata.MeasureHeader('time',
                                0.6,
                                100,
                                0.2,
                                's')
        self.assertRaises(Exception, fruits.check_header_update,
                          'new', np.array([1]), t2)
        self.assertRaises(Exception, fruits.check_header_update,
                          'rm', np.array([1]), undifferentiated)
        self.assertRaises(Exception, fruits.check_header_update,
                          'new', np.array([1]), chgandrmfruits)
        self.assertRaises(Exception, fruits.check_header_update,
                          'chg&rm', np.array([1]), chgandnewfruits1)
        
        print("Test 14: testing add_column method")
        flower = pd.Series(['rose', 'forgetmenot', 'waterlily'])
        weight = pd.Series([103, 97, 76, 15])
        wrongdimdes = xdata.DimensionDescription('flower', 'string')
        gooddimdes = xdata.DimensionDescription('weight', 'numeric', 'g')
        newfruits1 = fruits.add_column('weight', weight)
        newfruits2 = fruits.add_column(gooddimdes, weight)
        #testing Exceptions
        self.assertRaises(Exception, fruits.add_column, 'rose', 'forgetmenot')
        self.assertRaises(Exception, fruits.add_column, 'flower', flower)
        self.assertRaises(Exception, fruits.add_column, weight, weight)
        self.assertRaises(Exception, fruits.add_column, wrongdimdes, weight)
        #testing the result
        self.assertEqual(newfruits1.label, 'fruits')
        self.assertEqual(newfruits1.column_descriptors[3].label, 'weight')
        self.assertTrue(newfruits1.column_descriptors[3].unit is None)
        self.assertEqual(newfruits1.column_descriptors[3].dimensiontype,
                         'numeric')
        self.assertEqual(newfruits1.values[3][0], 103)
        self.assertEqual(newfruits2.label, 'fruits')
        self.assertEqual(newfruits2.column_descriptors[3].label, 'weight')
        self.assertEqual(newfruits2.column_descriptors[3].unit, 'g')
        self.assertEqual(newfruits2.column_descriptors[3].dimensiontype,
                         'numeric')
        self.assertEqual(newfruits2.values[3][2], 76)
        #making sure that the old header remains unchanged
        self.assertEqual(fruits.label, 'fruits')
        self.assertEqual(len(fruits.column_descriptors), 3)
        self.assertEqual(fruits.values.shape, (4, 3))
        print("Test 15: testing mergelines method")
        #testing Exceptions
        self.assertRaises(Exception, fruits.mergelines, 5)
        self.assertRaises(Exception, fruits.mergelines, ['apple'])
        self.assertRaises(Exception, fruits.mergelines, [0, 1, 23])
        self.assertRaises(Exception, fruits.mergelines, [-2])
        #testing the result
        colors = pd.Series([(0, 0, 0), (0, 0, 0), (0, 0, 0), (8, 8, 8)])
        newfruits = fruits.add_column('display', colors)
        series = newfruits.mergelines([0, 3])
        self.assertEqual(series[0], ['apple', 'cherry'])
        self.assertEqual(series[1], [0.5, 0.89])
        self.assertEqual(series[2], ['red'])
        self.assertEqual(series[3], (4, 4, 4))
        print("Test 16: testing the copy method")
        copyfruits = fruits2.copy()
        #testing that chaging one is not changing the other
        copyfruits = copyfruits.add_column('display', colors)
        print(fruits2.column_descriptors[2].dimensiontype)
        copyfruits.update_categoricalheader('new',
                                            None,
                                            [pd.Series(['kiwi',
                                                        0.89,
                                                        456,
                                                        (2, 89, 6)])])
        self.assertEqual(fruits2.getncolumns(), 3)
        self.assertEqual(copyfruits.getncolumns(), 4)
        self.assertEqual(fruits2.column_descriptors[2].dimensiontype, 'string')
        self.assertEqual(fruits2.values.shape, (4, 3))
        print("\n")
    
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
        print("Test 4: testing the __eq__ method")
        self.assertTrue(t == t2)
        self.assertFalse(x == t)
        print("Test 5: testing the __ne__ method")
        self.assertTrue(x!= t)
        self.assertFalse(t!=t2)
        print("Test 6: testing the getncolumns method")
        self.assertEqual(x.getncolumns(), 1)
        print("Test 7: testing the getunits method")
        self.assertEqual(x.getunits(), ['mm'])
        self.assertEqual(t.getunits(), ['s'])
        print("Test 8: testing the getallunits method")
        self.assertEqual(x.getallunits(), [[{'unit' : 'mm', 'value' : 1.0}]])
        self.assertEqual(t.getallunits(), [[{'unit' : 's', 'value' : 1.0}]])
        print("Test 9: testing the iscategorical, ismeasure, "
              "iscategoricalwithvalue, and isundifferentiated")
        self.assertFalse(x.iscategorical)
        self.assertTrue(x.ismeasure)
        self.assertFalse(x.iscategoricalwithvalues)
        self.assertFalse(x.isundifferentiated)
        print("Test 10: testing the getvalue method")
        self.assertEqual(x.getvalue(0), 1)
        self.assertEqual(x.getvalue(3,0), 2.5)
        self.assertRaises(Exception, x.getvalue, 3, 2)
        self.assertRaises(Exception, x.getvalue, 3, -1)
        self.assertRaises(Exception, x.getvalue, 'something')
        self.assertRaises(Exception, x.getvalue, -10)
        self.assertRaises(Exception, x.getvalue, 10)
        print("Test 11: testing the get_itemname method")
        self.assertRaises(Exception, x.get_itemname, 'coffee')
        self.assertRaises(Exception, x.get_itemname, 10)
        self.assertRaises(Exception, x.get_itemname, -10)
        self.assertRaises(Exception, x.get_itemname, ['chocolate', 'milk'])
        self.assertRaises(Exception, x.get_itemname, [10])
        self.assertEqual(x.get_itemname(0), 1)
        self.assertEqual(x.get_itemname([0]), [1])
        self.assertEqual(x.get_itemname([]), [])
        self.assertEqual(x.get_itemname([0, 1, 3, 2]), [1, 1.5, 2.5, 2.0])
        print("Test 12: testing the update_measureheader method")
        self.assertRaises(Exception, x.update_measureheader, 'orange')
        self.assertRaises(Exception, x.update_measureheader, n_elem = 'apple')
        self.assertRaises(Exception, x.update_measureheader, scale = 'cherry')
        self.assertEquals(x.update_measureheader(2).label, x.label)
        self.assertEquals(x.update_measureheader(2).start, 2)
        self.assertEquals(x.update_measureheader(n_elem = 0).n_elem, 0)
        self.assertEquals(x.update_measureheader(scale = 4).scale, 4)
        self.assertEquals(x.update_measureheader(2, 0).scale, 0.5)
        print("Test 13: testing check_header_update method")
        self.assertRaises(Exception,
                          x.check_header_update, 'hello', np.array([1]), x)
        self.assertRaises(Exception,
                          x.check_header_update, 'all', 'bonjour', x)
        self.assertRaises(Exception,
                          x.check_header_update, 'all', np.array([1]), 'hallo')
        self.assertRaises(Exception,
                          x.check_header_update, 'new', np.array([1]), x)
        self.assertRaises(Exception,
                          x.check_header_update, 'remove', np.array([1]), x)
        self.assertRaises(Exception,
                          x.check_header_update,
                          'chg',
                          np.array([[1]]),
                          x.update_measureheader(n_elem = 30))
        self.assertRaises(Exception,
                          x.check_header_update,
                          'chg&new',
                          np.array([[1], [2]]),
                          x)
        self.assertRaises(Exception,
                          x.check_header_update,
                          'chg&rm',
                          np.array([[1], [2]]),
                          x)
        print("Test 14: testing copy method")
        xcopy = x.copy()
        xcopy.update_measureheader(4, 5, 1)
        self.assertEqual(x.n_elem, 6)
        self.assertEqual(x.start, 1)
        self.assertEqual(x.scale, 0.5)
        print("\n")
        
    def test_xdata_module_Xdata_class(self):
        #creating the headers
        time = xdata.DimensionDescription('time', 'numeric', 's')
        t = xdata.MeasureHeader('time',
                                0.6,
                                5,
                                0.2,
                                column_descriptors = time)
        undifferentiated = xdata.CategoricalHeader('repetitions', n_elem = 3)
        dfvalues = pd.DataFrame([['apple', 0.5, 'red'],
                                 ['pear', 0.75, 'green'],
                                 ['banana', 0.66, 'yellow'],
                                 ['cherry', 0.89, 'red']])
        fruits = xdata.CategoricalHeader('fruits',
                                         ['fruits', 'fruitprices', 'colors'],
                                         4,
                                         dfvalues)
        #data
        data = np.random.rand(5, 3, 4)

        #the xdata instance
        setofdata = xdata.Xdata('name',
                                data,
                                [t, undifferentiated, fruits],
                                'm')
        print("Tests for the class Xdata (module xdata): \n")
        print("Test 1: attributes have the correct type")
        self.assertTrue(isinstance(setofdata.name, str))
        self.assertTrue(isinstance(setofdata.data, np.ndarray))
        self.assertTrue(isinstance(setofdata.headers, list))
        self.assertTrue(isinstance(setofdata.headers[1], xdata.Header))
        self.assertTrue(isinstance(setofdata.data_descriptor,
                                   xdata.DimensionDescription))
        print("Test 2: attributes have the correct value")
        self.assertEqual(setofdata.name, 'name')
        self.assertEqual(setofdata.data.shape, data.shape)
        self.assertEqual(setofdata.headers[0], t)
        self.assertEqual(setofdata.data_descriptor.label, 'name')
        self.assertEqual(setofdata.data_descriptor.unit, 'm')
        self.assertEqual(setofdata.data_descriptor.dimensiontype, 'numeric')
        print("Test 3: raising errors for arguments with wrong types")
        self.assertRaises(Exception,
                          xdata.Xdata,
                          1,
                          data,
                          [t, undifferentiated, fruits],
                          'm')
        self.assertRaises(Exception,
                          xdata.Xdata,
                          'xdata',
                          'yummy',
                          [t, undifferentiated, fruits],
                          'm')
        self.assertRaises(Exception,
                          xdata.Xdata,
                          'xdata',
                          data,
                          t,
                          'm')
        self.assertRaises(Exception,
                          xdata.Xdata,
                          'xdata',
                          data,
                          [t, undifferentiated, fruits],
                          125)
        self.assertRaises(Exception,
                          xdata.Xdata,
                          'xdata',
                          data,
                          [t, undifferentiated],
                          'm')
        self.assertRaises(Exception,
                          xdata.Xdata,
                          'xdata',
                          data,
                          [t, 'undifferentiated', fruits],
                          'm')
        print("Test 4: testing getndimensions method")
        self.assertEqual(setofdata.getndimensions(), 3)
        print("Test 5: testing shape method")
        self.assertEqual(setofdata.shape(), (5, 3, 4))
        print("Test 6: testing copy method")
        xdatacopy = setofdata.copy()
        self.assertEqual(xdatacopy.data_descriptor.allunits, 
                        setofdata.data_descriptor.allunits)
        series = [pd.Series(['kiwi', 0.95, 'brown']), 
                  pd.Series(['blueberry', '1.20', 'blue'])]
        addfruits = fruits.update_categoricalheader('new', None, series)
        slices = [np.random.rand(5, 3), np.random.rand(5, 3)]
        (xdatacopy, flag) = setofdata.update_xdata('new',
                                                   2,
                                                   None,
                                                   slices,
                                                   addfruits)
        self.assertEqual(xdatacopy.shape(), (5, 3, 6))
        self.assertEqual(setofdata.shape(), (5, 3, 4))
        self.assertEqual(setofdata.headers[2], fruits)                
        print("Test 7: testing the update_data method")
        newdata1 = np.random.rand(5, 3, 4)
        udsetofdata1 = setofdata.update_data(newdata1)
        newdata2 = np.random.rand(10, 8, 4)
        udsetofdata2 = setofdata.update_data(newdata2)
        self.assertEqual(udsetofdata1.getndimensions(), 3)
        self.assertEqual(udsetofdata2.getndimensions(), 3)
        self.assertEqual(udsetofdata1.shape(), (5, 3, 4))
        self.assertEqual(udsetofdata2.shape(), (10, 8, 4))
        self.assertEqual(udsetofdata1.headers[0].n_elem, 5)
        self.assertEqual(udsetofdata2.headers[0].n_elem, 10)
        self.assertEqual(udsetofdata1.headers[1].n_elem, 3)
        self.assertEqual(udsetofdata2.headers[1].n_elem, 8)
        self.assertEqual(udsetofdata1.headers[2].n_elem, 4)
        self.assertEqual(udsetofdata2.headers[2].n_elem, 4)
        self.assertRaises(Exception,
                          setofdata.update_data,
                          np.random.rand(5, 3, 4, 5))
        self.assertRaises(Exception,
                          setofdata.update_data,
                          np.random.rand(5, 3, 9))
        print("Test 8: testing the update_xdata method")
        #if dim is not an int of out of range, it raises an exception 
        newfruits = fruits.update_categoricalheader('chg', [1, 3], series)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 'yummy', None, newdata1, newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 4, None, newdata1, newfruits)
        #flag 'all' that should be a 'chgdata' flag (because the header
        #hasn't changed)
        (alltochgdataxdata, flag) = setofdata.update_xdata('all',
                                                           1,
                                                           None,
                                                           newdata1,
                                                           undifferentiated)
        self.assertEqual(flag, 'chgdata')
        self.assertEqual(alltochgdataxdata.data[0][0][0], newdata1[0][0][0])
        self.assertEqual(setofdata.data[0][0][0], data[0][0][0])
        
        #flag 'all'  (not all exceptions are tested)
        (allxdata, flag) = setofdata.update_xdata('all',
                                                  2,
                                                  None,
                                                  newdata1,
                                                  newfruits)
        self.assertEqual(flag, 'all')
        self.assertEqual(allxdata.headers[2].values[0][1], 'kiwi')
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 2, 'yummy', newdata1, newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 2, [1], newdata1, 'yummy')
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 2, [1], 'yummy', newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 2, [1], np.random.rand(5, 3, 4, 2), newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 2, [1], np.random.rand(5, 8, 4), newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'all', 2, [1], np.random.rand(5, 3, 7), newfruits)
        #flag 'chgdata'
        (chgdataxdata, flag) = setofdata.update_xdata('chgdata',
                                                      1,
                                                      None,
                                                      newdata1,
                                                      None)
        self.assertEqual(flag, 'chgdata')
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chgdata', 'yummy', None, newdata1, None)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chgdata', 0, 'yummy', newdata1, None)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chgdata', 0, None, 'yummy', None)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chgdata', 0, None, newdata1, newfruits)
        #flag 'chg'  (not all exceptions are tested)
        (chgxdata, flag) = setofdata.update_xdata('chg',
                                                  2,
                                                  [1, 3],
                                                  slices,
                                                  newfruits)
        self.assertEqual(chgxdata.data[3][0][1], slices[0][3][0])
        self.assertEqual(flag, 'chg')
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 0, [0, 1], slices,
                          xdata.MeasureHeader('time', 0.6, 5, 2, 
                                              column_descriptors = time))
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 0, [0, 1], slices, newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 3, [0, 1], slices, t)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 3, 0, slices, newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 3, [0, 1], 'yummy', newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 3, [0, 1, 2], slices, newfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 3, [0], [np.random.rand(5, 4)], fruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg', 3, [1, 3], slices, 
                          fruits.update_categoricalheader('new', None, series))
        #flag 'new'  (not all exceptions are tested)
        addfruits = fruits.update_categoricalheader('new', None, series)
        (newxdata, flag) = setofdata.update_xdata('new',
                                                  2,
                                                  None,
                                                  slices,
                                                  addfruits)
        self.assertEqual(newxdata.data[0][0][0], setofdata.data[0][0][0])
        self.assertEqual(newxdata.data[0][0][5], slices[1][0][0])
        self.assertEqual(flag, 'new')
        self.assertEqual(newxdata.shape(), (5, 3, 6))
        self.assertRaises(Exception, setofdata.update_xdata,
                          'new', 0, None, slices, addfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'new', 2, 'yummy', slices, addfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'new', 2, None, slices[0], addfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'new', 2, None, 'yummy', addfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'new', 2, None, slices, 'yummy')
        #flag 'remove' (not all exceptions are tested)
        rmfruits = fruits.update_categoricalheader('remove', [1, 3], None)
        (rmxdata, flag) = setofdata.update_xdata('remove',
                                                  2,
                                                  [1, 3],
                                                  None,
                                                  rmfruits)
        self.assertEqual(flag, 'remove')
        self.assertEqual(rmxdata.shape(), (5, 3, 2))
        self.assertRaises(Exception, setofdata.update_xdata,
                          'remove', 2, [1], None, rmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'remove', 0, [1,3], None, rmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'remove', 2, [1,3], None, 'yummy')
        self.assertRaises(Exception, setofdata.update_xdata,
                          'remove', 2, [1,'yummy'], None, rmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'remove', 2, [1,3], [1,3], rmfruits)
        #flag 'chg&new' (not all exceptions are tested)
        chgandnewfruits = fruits.update_categoricalheader('chg&new',
                                                          [[0,1], None],
                                                          [series, series])
        (chgandnewxdata, flag) = setofdata.update_xdata('chg&new',
                                                        2,
                                                        [0, 1],
                                                        [slices, slices],
                                                        chgandnewfruits)
        self.assertEqual(flag, 'chg&new')
        self.assertEqual(chgandnewxdata.shape(), (5, 3, 6))
        self.assertEqual(chgandnewxdata.data[0][0][5], slices[1][0][0])
        self.assertEqual(chgandnewxdata.data[0][0][2], setofdata.data[0][0][2])
        self.assertEqual(chgandnewxdata.data[0][0][0], slices[0][0][0])
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 1], 'yummy'],
                          [slices, slices], chgandnewfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [],
                          [slices, slices], chgandnewfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 'yummy'], None],
                          [slices, slices], chgandnewfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 1, 3], None],
                          [slices, slices], chgandnewfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [slices], chgandnewfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          'yummy', chgandnewfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [series, slices], chgandnewfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [slices, slices], fruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [slices, slices], 'yummy')
        # flag 'chg&rm' (not all exceptions are tested)
        chgandrmfruits = fruits.update_categoricalheader('chg&rm',
                                                          [[0,1], [3]],
                                                          series)
        (chgandrmxdata, flag) = setofdata.update_xdata('chg&rm',
                                                        2,
                                                        [[0, 1], [3]],
                                                        slices,
                                                        chgandrmfruits)
        self.assertEqual(flag, 'chg&rm')
        self.assertEqual(chgandrmxdata.shape(), (5, 3, 3))
        self.assertEqual(chgandrmxdata.data[0][0][2], setofdata.data[0][0][2])
        self.assertEqual(chgandrmxdata.data[0][0][0], slices[0][0][0])
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 'yummy'], [3]],
                          slices, chgandrmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 1], ['yummy']],
                          slices, chgandrmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 1]],
                          slices, chgandrmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 1], [3]],
                          'yummy', chgandrmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 1], [3]],
                          slices, 'yummy')
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 1, 2], [3]],
                          slices, chgandrmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 1], [3, 2]],
                          slices, chgandrmfruits)
        self.assertRaises(Exception, setofdata.update_xdata,
                          'chg&rm', 2, [[0, 5], [3]],
                          slices, chgandrmfruits)
        # flag 'perm' (not all exceptions are tested)
        (permxdata, flag) = setofdata.update_xdata('perm',
                                                   2,
                                                   [0, 3, 2, 1],
                                                   None,
                                                   fruits)
        self.assertEqual(flag, 'perm')
        self.assertEqual(permxdata.shape(), (5, 3, 4))
        self.assertEqual(permxdata.data[2][0][0], setofdata.data[2][0][0])
        self.assertEqual(permxdata.data[0][0][2], setofdata.data[0][0][2])
        self.assertEqual(permxdata.data[0][2][1], setofdata.data[0][2][3])
        
        print("Test 9: testing the modify_dimensions method")
        #flag 'global'
        (globalxdata, flag) = setofdata.modify_dimensions('global',
                                                          None,
                                                          np.random.rand(4, 5),
                                                          [fruits, t])
        self.assertEqual(flag, 'global')
        self.assertEqual(globalxdata.name, setofdata.name)
        self.assertEqual(globalxdata.data_descriptor.allunits,
                         setofdata.data_descriptor.allunits)
        self.assertEqual(globalxdata.headers[0], fruits)
        self.assertRaises(Exception, setofdata.modify_dimensions,
                          'global', 'yummy', np.random.rand(4, 5), [fruits, t])
        self.assertRaises(Exception, setofdata.modify_dimensions,
                          'global', None, np.random.rand(4, 5), [fruits])
        self.assertRaises(Exception, setofdata.modify_dimensions,
                          'global', None, 'yummy', [fruits, t])
        print("\n")
    
    def test_xdata_module_createDimensionDescription_function(self):
        print("Test for the createDimensionDescription function \
        (module xdata) \n")
        #checking the Exceptions
        self.assertRaises(Exception, xdata.createDimensionDescription, 1, 1)
        self.assertRaises(Exception,
                          xdata.createDimensionDescription,'fruits', 1)
        self.assertRaises(Exception,
                          xdata.createDimensionDescription,
                          'fruits',
                          pd.DataFrame([['apple', 0.5],
                                        ['pear', 0.75],
                                        ['banana', 0.66],
                                        ['cherry', 0.89]]))
        #creating DimensionDescription instances with the function
        c = xdata.createDimensionDescription('cars')
        fruits = pd.Series(['apple', 'pear', 'banana'])
        f = xdata.createDimensionDescription ('fruits', fruits)
        mix = pd.Series(['apple', int(3), 'banana'])
        m = xdata.createDimensionDescription ('mix', mix)
        #creating  DimensionDescription instances without the function
        cdd = xdata.DimensionDescription('cars', 'mixed')
        fdd = xdata.DimensionDescription('fruits', 'string')
        mdd = xdata.DimensionDescription('mix', 'mixed')
        #asserting that both instances are the same
        self.assertEqual(c.label, cdd.label)
        self.assertEqual(c.dimensiontype, cdd.dimensiontype)
        self.assertEqual(m.label, mdd.label)
        self.assertEqual(m.dimensiontype, mdd.dimensiontype)
        self.assertEqual(f.label, fdd.label)
        self.assertEqual(f.dimensiontype, fdd.dimensiontype)
       
             
if __name__ == "__main__":    
    firsttest = MyTestCase()
    firsttest.test_xdata_module_DimensionDescription_class()
    firsttest.test_xdata_module_CategoricalHeader_class()
    firsttest.test_xdata_module_MeasureHeader_class()
    firsttest.test_xdata_module_Xdata_class()
    firsttest.test_xdata_module_createDimensionDescription_function()
    