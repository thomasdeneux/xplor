
"""tests module is a module to test the others

The modules that need to be tested are:
    - xdata (shape of the data itself)

This module uses:
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
        r = xdata.DimensionDescription('race_times', 'numeric',
                                       ['s', 1, 'ms', 0.001, 'min', 60, 'hour',
                                        3600])
        f = xdata.DimensionDescription('fruits', 'string')

        print("Tests for the class DimensionDescriptions (module xdata): \n")

        print("Test 1: attributes have the correct type")
        # test sur prices (p)
        self.assertTrue(isinstance(p.label, str))
        self.assertTrue(isinstance(p.dimension_type, str))
        self.assertTrue(isinstance(p.unit, str))
        self.assertTrue(isinstance(p.all_units, list))
        self.assertTrue(isinstance(p.all_units[0], dict))
        self.assertTrue(isinstance(p.all_units[0]['unit'], str))
        self.assertTrue(isinstance(p.all_units[0]['value'], float))
        # test sur race_times (r)
        self.assertTrue(isinstance(r.label, str))
        self.assertTrue(isinstance(r.dimension_type, str))
        self.assertTrue(isinstance(r.unit, str))
        self.assertTrue(isinstance(r.all_units, list))
        self.assertTrue(isinstance(r.all_units[2], dict))
        self.assertTrue(isinstance(r.all_units[2]['unit'], str))
        self.assertTrue(isinstance(r.all_units[2]['value'], float))
        # test sur fruits (f)
        self.assertTrue(isinstance(f.label, str))
        self.assertTrue(isinstance(f.dimension_type, str))
        self.assertTrue(f.unit is None)
        self.assertTrue(f.all_units is None)
        print("Test 2: attributes have the correct value")
        # test sur prices (p)
        self.assertEqual(p.label, 'prices')
        self.assertEqual(p.dimension_type, 'numeric')
        self.assertEqual(p.unit, 'euros')
        self.assertEqual(p.all_units, [{'unit': 'euros', 'value': 1}])
        # test sur race_times (r)
        self.assertEqual(r.label, 'race_times')
        self.assertEqual(r.dimension_type, 'numeric')
        self.assertEqual(r.unit, 's')
        self.assertEqual(r.all_units, [{'unit': 'ms', 'value': 0.001},
                                       {'unit': 's', 'value': 1.0},
                                       {'unit': 'min', 'value': 60.0},
                                       {'unit': 'hour', 'value': 3600.0}])
        # test sur fruits (f)
        self.assertEqual(f.label, 'fruits')
        self.assertEqual(f.dimension_type, 'string')
        self.assertEqual(f.unit, None)
        self.assertEqual(f.all_units, None)
        print("Test 3: raising errors for arguments with wrong types")
        # test sur prices (p)
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
                          'numeric', ['s', 0.001, 'ms', 0.000001])
        self.assertRaises(Exception, xdata.DimensionDescription, 'prices',
                          'numeric', {'s': 1})
        print("Test 4: method infertype")
        # no getdefaultvalue
        self.assertTrue(xdata.DimensionDescription.infertype(0), 'numeric')
        self.assertTrue(xdata.DimensionDescription.infertype(0.03), 'numeric')
        self.assertTrue(xdata.DimensionDescription.infertype('bla-bla'),
                        'string')
        self.assertTrue(xdata.DimensionDescription.infertype([]), 'mixed')
        self.assertTrue(xdata.DimensionDescription.infertype(True), 'logical')
        self.assertTrue(xdata.DimensionDescription.infertype((1, 12, 200),
                                                             'color'))
        self.assertTrue(xdata.DimensionDescription.infertype((-1, 12, 200),
                                                             'mixed'))
        self.assertTrue(xdata.DimensionDescription.infertype((1, 12, 275),
                                                             'mixed'))
        # get_default_value = False
        self.assertTrue(xdata.DimensionDescription.infertype(0, False),
                        'numeric')
        # getdefaultvalue = True
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
        print("Test 6: method set_dimtype_to_mixed")
        f.set_dimtype_to_mixed()
        self.assertEqual(f.dimension_type, 'mixed')
        print("Test 7: method copy")
        p_copy = p.copy()
        r_copy = r.copy()
        f_copy = f.copy()
        self.assertEqual(p_copy.all_units, [{'unit': 'euros', 'value': 1}])
        self.assertEqual(r_copy.all_units, [{'unit': 'ms', 'value': 0.001},
                                            {'unit': 's', 'value': 1.0},
                                            {'unit': 'min', 'value': 60.0},
                                            {'unit': 'hour', 'value': 3600.0}])
        self.assertTrue(f_copy.all_units is None)
        print("\n")

    def test_xdata_module_CategoricalHeader_class(self):
        print("Tests for the class CategoricalHeader (module xdata):")
        print("\n")
        df_values = pd.DataFrame([['apple', 0.5, 'red'],
                                 ['pear', 0.75, 'green'],
                                 ['banana', 0.66, 'yellow'],
                                 ['cherry', 0.89, 'red']])
        fruits = xdata.CategoricalHeader('fruits',
                                         ['fruits', 'fruit_prices', 'colors'],
                                         4,
                                         df_values)
        fruits3 = xdata.CategoricalHeader('fruits',
                                          ['fruits', 'fruit_prices', 'colors'],
                                          4,
                                          df_values)
        fruit_prices = xdata.DimensionDescription('prices',
                                                  'numeric',
                                                  'euros/kg')
        fruits2 = xdata.CategoricalHeader('fruits',
                                          ['fruits', fruit_prices, 'colors'],
                                          values=df_values)
        undifferentiated = xdata.CategoricalHeader('repetitions', n_elem=10)

        print("Test 1: attributes have the correct type")
        # tests for fruits
        self.assertTrue(isinstance(fruits.label, str))
        self.assertTrue(isinstance(fruits.column_descriptors, list))
        self.assertTrue(isinstance(fruits.column_descriptors[0],
                                   xdata.DimensionDescription))
        self.assertTrue(isinstance(fruits.n_elem, int))
        self.assertTrue(isinstance(fruits.values, pd.core.frame.DataFrame))
        # tests for fruits2
        self.assertTrue(isinstance(fruits2.label, str))
        self.assertTrue(isinstance(fruits2.column_descriptors, list))
        self.assertTrue(isinstance(fruits2.column_descriptors[0],
                                   xdata.DimensionDescription))
        self.assertTrue(isinstance(fruits2.n_elem, int))
        self.assertTrue(isinstance(fruits2.values, pd.core.frame.DataFrame))
        # tests for undifferentiated
        self.assertTrue(isinstance(undifferentiated.label, str))
        self.assertTrue(undifferentiated.column_descriptors is None)
        self.assertTrue(isinstance(undifferentiated.n_elem, int))
        self.assertTrue(isinstance(undifferentiated.values,
                                   pd.core.frame.DataFrame))
        print("Test 2: attributes have the correct value")
        # tests for fruits
        self.assertEqual(fruits.label, 'fruits')
        self.assertEqual(fruits.column_descriptors[0].label,
                         xdata.DimensionDescription('fruits', 'string').label)
        self.assertEqual(fruits.column_descriptors[0].dimension_type,
                         xdata.DimensionDescription('fruits',
                                                    'string').dimension_type)
        self.assertEqual(fruits.column_descriptors[1].label,
                         xdata.DimensionDescription('fruit_prices',
                                                    'numeric').label)
        self.assertEqual(fruits.column_descriptors[1].dimension_type,
                         xdata.DimensionDescription('fruit_prices',
                                                    'numeric').dimension_type)
        self.assertEqual(fruits.column_descriptors[2].label,
                         xdata.DimensionDescription('colors',
                                                    'string').label)
        self.assertEqual(fruits.column_descriptors[2].dimension_type,
                         xdata.DimensionDescription('colors',
                                                    'string').dimension_type)
        self.assertEqual(fruits.n_elem, 4)
        self.assertEqual(fruits.values[0][0], 'apple')
        self.assertEqual(fruits.values[1][0], 0.5)
        self.assertEqual(fruits.values[2][3], 'red')
        # tests for fruits2
        self.assertEqual(fruits2.label, 'fruits')
        self.assertEqual(fruits2.column_descriptors[0].label,
                         xdata.DimensionDescription('fruits', 'string').label)
        self.assertEqual(fruits2.column_descriptors[0].dimension_type,
                         xdata.DimensionDescription('fruits',
                                                    'string').dimension_type)
        self.assertEqual(fruits2.column_descriptors[1].label,
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').label)
        self.assertEqual(fruits2.column_descriptors[1].dimension_type,
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').dimension_type)
        self.assertEqual(fruits2.column_descriptors[1].unit,
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').unit)
        self.assertEqual(fruits2.column_descriptors[1].all_units,
                         xdata.DimensionDescription('prices',
                                                    'numeric',
                                                    'euros/kg').all_units)
        self.assertEqual(fruits2.column_descriptors[2].label,
                         xdata.DimensionDescription('colors',
                                                    'string').label)
        self.assertEqual(fruits2.column_descriptors[2].dimension_type,
                         xdata.DimensionDescription('colors',
                                                    'string').dimension_type)
        self.assertEqual(fruits2.n_elem, 4)
        self.assertEqual(fruits2.values[0][0], 'apple')
        self.assertEqual(fruits2.values[1][0], 0.5)
        self.assertEqual(fruits2.values[2][3], 'red')
        # tests for undifferentiated
        self.assertEqual(undifferentiated.label, 'repetitions')
        self.assertEqual(undifferentiated.n_elem, 10)
        self.assertEqual(undifferentiated.values.shape, (10, 0))
        print("Test 3: raising errors for arguments with wrong types")
        self.assertRaises(Exception, xdata.CategoricalHeader, 1)
        self.assertRaises(Exception, xdata.CategoricalHeader, 'label')
        self.assertRaises(Exception,
                          xdata.CategoricalHeader, 'label', n_elem='n_elem')
        self.assertRaises(Exception,
                          xdata.CategoricalHeader, 'label', n_elem=1,
                          column_descriptors=['str'])
        self.assertRaises(Exception,
                          xdata.CategoricalHeader, 'label', values=[1, 2, 3])
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem=1,
                          values=df_values)
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem='n_elem',
                          values=df_values)
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem=1,
                          values=df_values,
                          column_descriptors=[])
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem=1,
                          values=df_values,
                          column_descriptors=56)
        self.assertRaises(Exception,
                          xdata.CategoricalHeader,
                          'label',
                          n_elem=1,
                          values=df_values,
                          column_descriptors=['fruits', 45])
        print("Test 4: testing the __eq__ method")
        self.assertTrue(fruits == fruits3)
        self.assertFalse(fruits == fruits2)
        print("Test 5: testing the __ne__ method")
        self.assertTrue(fruits != fruits2)
        self.assertFalse(fruits != fruits3)
        print("Test 6: testing the get_n_columns method")
        self.assertEqual(fruits.get_n_columns(), 3)
        self.assertEqual(undifferentiated.get_n_columns(), 0)
        print("Test 7: testing the get_units method")
        self.assertEqual(undifferentiated.get_units(), [])
        self.assertEqual(fruits.get_units(), ['no unit', 'no unit', 'no unit'])
        self.assertEqual(fruits2.get_units(),
                         ['no unit', 'euros/kg', 'no unit'])
        print("Test 8: testing the get_all_units method")
        self.assertEqual(undifferentiated.get_all_units(), [])
        self.assertEqual(fruits.get_all_units(),
                         ['no unit', 'no unit', 'no unit'])
        self.assertEqual(fruits2.get_all_units(),
                         ['no unit',
                          [{'unit': 'euros/kg', 'value': 1}],
                          'no unit'])
        print("Test 9: testing the is_categorical, is_measure, "
              "is_categorical_with_value, and is_undifferentiated")
        self.assertTrue(fruits.is_categorical)
        self.assertTrue(undifferentiated.is_categorical)
        self.assertFalse(fruits.is_measure)
        self.assertFalse(undifferentiated.is_measure)
        self.assertTrue(fruits.is_categorical_with_values)
        self.assertFalse(undifferentiated.is_categorical_with_values)
        self.assertFalse(fruits.is_undifferentiated)
        self.assertTrue(undifferentiated.is_undifferentiated)
        print("Test 10: testing the get_value method")
        self.assertEqual(undifferentiated.get_value(0), 0)
        self.assertEqual(fruits.get_value(2, 1), 0.66)
        self.assertEqual(fruits.get_value(2), 'banana')
        self.assertEqual(fruits.get_value(2, 'fruits'), 'banana')
        self.assertRaises(Exception, fruits.get_value, '2')
        self.assertRaises(Exception, fruits.get_value, -3)
        self.assertRaises(Exception, fruits.get_value, 10)
        print("Test 11: testing the get_item_name method")
        self.assertRaises(Exception, fruits.get_item_name, 'coffee')
        self.assertRaises(Exception, fruits.get_item_name, 10)
        self.assertRaises(Exception, fruits.get_item_name, -10)
        self.assertRaises(Exception, fruits.get_item_name,
                          ['chocolate', 'milk'])
        self.assertRaises(Exception, fruits.get_item_name, [10])
        self.assertEqual(fruits.get_item_name(0), 'apple')
        self.assertEqual(fruits.get_item_name([0]), ['apple'])
        self.assertEqual(fruits.get_item_name([]), [])
        self.assertEqual(fruits.get_item_name([0, 1, 3, 2]),
                         ['apple',
                          'pear',
                          'cherry',
                          'banana'])
        print("Test 12: testing the update_measure_header method")
        wrong_size_col = pd.DataFrame([['apple', 0.5, 'red', 'yummy'],
                                      ['pear', 0.75, 'green', 'yummy'],
                                      ['banana', 0.66, 'yellow', 'yummy'],
                                      ['cherry', 0.89, 'red', 'yummy']])
        wrong_dimtype = pd.DataFrame([['apple', '0.5', 'red'],
                                      ['pear', 0.75, 'green'],
                                      ['banana', 0.66, 'yellow'],
                                      ['cherry', 0.89, 'red']])
        # testing for flag 'all'
        all_fruits = fruits.update_categorical_header('all', None,
                                                      wrong_dimtype)
        self.assertEqual(all_fruits.label, fruits.label)
        self.assertEqual(all_fruits.column_descriptors[1].dimension_type,
                         'mixed')
        self.assertEqual(all_fruits.values.shape, (4, 3))
        self.assertRaises(Exception,
                          fruits.update_categorical_header,
                          'all',
                          [2, 4],
                          df_values)
        self.assertRaises(Exception,
                          fruits.update_categorical_header,
                          'all',
                          None,
                          [1, 2, 3])
        self.assertRaises(Exception,
                          fruits.update_categorical_header,
                          'all',
                          None,
                          wrong_size_col)
        # testing for flag 'new'
        series = [pd.Series(['kiwi', 0.95, 'brown']),
                  pd.Series(['blueberry', '1.20', 'blue'])]
        new_fruits = fruits.update_categorical_header('new', None, series)
        self.assertEqual(new_fruits.label, fruits.label)
        self.assertEqual(new_fruits.column_descriptors[1].dimension_type,
                         'mixed')
        self.assertEqual(new_fruits.values.shape, (6, 3))
        self.assertEqual(new_fruits.values[1][5], '1.20')
        self.assertEqual(new_fruits.values[0][4], 'kiwi')
        self.assertEqual(new_fruits.values[1][4], 0.95)
        self.assertRaises(Exception,
                          fruits.update_categorical_header,
                          'new', 1, series)
        self.assertRaises(Exception,
                          fruits.update_categorical_header,
                          'new', [], pd.Series(['kiwi', 0.95, 'brown']))
        self.assertRaises(Exception,
                          fruits.update_categorical_header,
                          'new', [], [1, 2])
        self.assertRaises(Exception,
                          fruits.update_categorical_header,
                          'new',
                          [],
                          [pd.Series(['kiwi', 0.95, 'brown', 'yummy']),
                           pd.Series(['blueberry', '1.20', 'blue', 'yummy'])])
        # testing for flag 'chg'
        chg_fruits = fruits.update_categorical_header('chg', [1, 3], series)
        self.assertEqual(chg_fruits.label, fruits.label)
        self.assertEqual(chg_fruits.column_descriptors[1].dimension_type,
                         'mixed')
        self.assertEqual(chg_fruits.values.shape, (4, 3))
        self.assertEqual(chg_fruits.values[1][3], '1.20')
        self.assertEqual(chg_fruits.values[0][1], 'kiwi')
        self.assertEqual(chg_fruits.values[1][1], 0.95)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg', 1, series)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg', [1], 'yummy')
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg', [1, -3], series)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg', [122, 1], series)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg', ['14', 1], series)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg', [1], ['yummy'])
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg', [1, 2],
                          [pd.Series(['kiwi', 0.95, 'brown', 'yummy']),
                           pd.Series(['blueberry', '1.20', 'blue', 'yummy'])])
        # testing for flag 'remove'
        remove_fruits = fruits.update_categorical_header('remove', [2], [])
        self.assertEqual(remove_fruits.label, fruits.label)
        self.assertEqual(remove_fruits.values.shape, (3, 3))
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'remove', 1, None)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'remove', [12], None)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'remove', [-1], None)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'remove', ['yummy'], None)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'remove', [1], [1])
        # testing for flag 'perm'
        perm_fruits = fruits.update_categorical_header('perm', [1, 2, 3, 0],
                                                       None)
        self.assertEqual(perm_fruits.label, fruits.label)
        self.assertEqual(perm_fruits.values[0][1], fruits.values[0][2])
        self.assertEqual(perm_fruits.values[1][3], fruits.values[1][0])
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'perm', [1, 2, 3, 0], [1])
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'perm', 'yummy', None)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'perm', [1, 2], None)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'perm', ['yummy', 2, 3, 0], None)
        # testing for flag 'chg&new'
        chg_and_new_fruits1 = fruits.update_categorical_header(
            'chg&new', [1, 2], [series, series])
        chg_and_new_fruits2 = fruits.update_categorical_header(
            'chg&new', [[3, 2], []], [series, series])
        self.assertEquals(chg_and_new_fruits1.label,
                          fruits.label,
                          chg_and_new_fruits2.label)
        self.assertEquals(len(chg_and_new_fruits1.column_descriptors),
                          len(fruits.column_descriptors),
                          len(chg_and_new_fruits2.column_descriptors))
        self.assertEquals(chg_and_new_fruits1.values.shape,
                          chg_and_new_fruits2.values.shape,
                          (6, 3))
        self.assertEqual(chg_and_new_fruits1.values[0][1], 'kiwi')
        self.assertEqual(chg_and_new_fruits1.values[0][2], 'blueberry')
        self.assertEqual(chg_and_new_fruits1.values[0][4], 'kiwi')
        self.assertEqual(chg_and_new_fruits1.values[0][5], 'blueberry')
        self.assertEqual(chg_and_new_fruits2.values[0][3], 'kiwi')
        self.assertEqual(chg_and_new_fruits2.values[0][2], 'blueberry')
        self.assertEqual(chg_and_new_fruits2.values[0][4], 'kiwi')
        self.assertEqual(chg_and_new_fruits2.values[0][5], 'blueberry')
        self.assertEquals(
            chg_and_new_fruits1.column_descriptors[1].dimension_type,
            chg_and_new_fruits2.column_descriptors[1].dimension_type,
            'mixed')
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg&new', 1, [series, series])
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg&new', [1, 2], 'yummy')
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg&new', [1, 2], series)
        # testing for flag 'chg&rm'
        chg_and_rm_fruits = fruits.update_categorical_header(
            'chg&rm', [[1, 2], [0]], series)
        self.assertEqual(chg_and_rm_fruits.label, fruits.label)
        self.assertEqual(chg_and_rm_fruits.get_n_columns(),
                         fruits.get_n_columns())
        self.assertEqual(chg_and_rm_fruits.values.shape, (3, 3))
        self.assertEqual(chg_and_rm_fruits.values[0][0], 'kiwi')
        self.assertEqual(chg_and_rm_fruits.values[0][1], 'blueberry')
        self.assertEqual(chg_and_rm_fruits.values[0][2], 'cherry')
        self.assertEquals(
            chg_and_rm_fruits.column_descriptors[1].dimension_type, 'mixed')
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg&rm', 1, series)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg&rm', [1, 2, 3], series)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg&rm', [1, 2], series)
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'chg&rm', [[1, 2], []], 'yummy')
        # testing for not a flag or a flag that is not accepted by the method
        self.assertRaises(Exception, fruits.update_categorical_header,
                          'dim_chg', [], [])
        print("Test 13: testing check_header_update method")
        # this method is a test itself, it does not return anything, it only
        # raises exceptions when there is an obvious problem (not a good name,
        # not a good size)
        # We conduct a few tests on this testing methods, but the method is not
        # fully covered
        self.assertRaises(Exception, fruits.check_header_update,
                          'yummy', np.array([1]), chg_and_rm_fruits)
        self.assertRaises(Exception, fruits.check_header_update,
                          'new', [], chg_and_rm_fruits)
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
                          'new', np.array([1]), chg_and_rm_fruits)
        self.assertRaises(Exception, fruits.check_header_update,
                          'chg&rm', np.array([1]), chg_and_new_fruits1)

        print("Test 14: testing add_column method")
        flower = pd.Series(['rose', 'forgetmenot', 'waterlily'])
        weight = pd.Series([103, 97, 76, 15])
        wrong_dim_des = xdata.DimensionDescription('flower', 'string')
        good_dim_des = xdata.DimensionDescription('weight', 'numeric', 'g')
        new_fruits1 = fruits.add_column('weight', weight)
        new_fruits2 = fruits.add_column(good_dim_des, weight)
        # testing Exceptions
        self.assertRaises(Exception, fruits.add_column, 'rose', 'forgetmenot')
        self.assertRaises(Exception, fruits.add_column, 'flower', flower)
        self.assertRaises(Exception, fruits.add_column, weight, weight)
        self.assertRaises(Exception, fruits.add_column, wrong_dim_des, weight)
        # testing the result
        self.assertEqual(new_fruits1.label, 'fruits')
        self.assertEqual(new_fruits1.column_descriptors[3].label, 'weight')
        self.assertTrue(new_fruits1.column_descriptors[3].unit is None)
        self.assertEqual(new_fruits1.column_descriptors[3].dimension_type,
                         'numeric')
        self.assertEqual(new_fruits1.values[3][0], 103)
        self.assertEqual(new_fruits2.label, 'fruits')
        self.assertEqual(new_fruits2.column_descriptors[3].label, 'weight')
        self.assertEqual(new_fruits2.column_descriptors[3].unit, 'g')
        self.assertEqual(new_fruits2.column_descriptors[3].dimension_type,
                         'numeric')
        self.assertEqual(new_fruits2.values[3][2], 76)
        # making sure that the old header remains unchanged
        self.assertEqual(fruits.label, 'fruits')
        self.assertEqual(len(fruits.column_descriptors), 3)
        self.assertEqual(fruits.values.shape, (4, 3))
        print("Test 15: testing merge_lines method")
        # testing Exceptions
        self.assertRaises(Exception, fruits.merge_lines, 5)
        self.assertRaises(Exception, fruits.merge_lines, ['apple'])
        self.assertRaises(Exception, fruits.merge_lines, [0, 1, 23])
        self.assertRaises(Exception, fruits.merge_lines, [-2])
        # testing the result
        colors = pd.Series([xdata.Color((0, 0, 0)), xdata.Color((0, 0, 0)),
                            xdata.Color((0, 0, 0)), xdata.Color((8, 8, 8))])
        new_fruits = fruits.add_column('display', colors)
        series = new_fruits.merge_lines([0, 3])
        self.assertEqual(series[0], ['apple', 'cherry'])
        self.assertEqual(series[1], [0.5, 0.89])
        self.assertEqual(series[2], ['red'])
        self.assertEqual(series[3], xdata.Color((4, 4, 4)))
        print("Test 16: testing the copy method")
        copy_fruits = fruits2.copy()
        # testing that changing one is not changing the other
        copy_fruits = copy_fruits.add_column('display', colors)
        copy_fruits.update_categorical_header('new',
                                              None,
                                              [pd.Series(['kiwi', 0.89,
                                                          456, (2, 89, 6)])])
        self.assertEqual(fruits2.get_n_columns(), 3)
        self.assertEqual(copy_fruits.get_n_columns(), 4)
        self.assertEqual(fruits2.column_descriptors[2].dimension_type,
                         'string')
        self.assertEqual(fruits2.values.shape, (4, 3))
        print("\n")

    def test_xdata_module_MeasureHeader_class(self):
        x = xdata.MeasureHeader('x', 1, 6, 0.5, 'mm')
        # TODO get unit from bank and also path when it fails to find a
        # correspondence
        # y = xdata.MeasureHeader('y', 1, 0, 0.5, 'mm', True)
        time = xdata.DimensionDescription('time', 'numeric', 's')
        t = xdata.MeasureHeader('time',
                                0.6,
                                100,
                                0.2,
                                column_descriptors=time)
        t2 = xdata.MeasureHeader('time',
                                 0.6,
                                 100,
                                 0.2,
                                 's')
        print("Tests for the class MeasureHeader (module xdata): \n")
        print("Test 1: attributes have the correct type")
        self.assertTrue(isinstance(x.label, str))
        self.assertTrue(isinstance(x.scale, float))
        self.assertTrue(isinstance(x.start, float))
        self.assertTrue(isinstance(x.n_elem, int))
        self.assertTrue(isinstance(x.column_descriptors, list))
        self.assertTrue(isinstance(x.column_descriptors[0],
                                   xdata.DimensionDescription))
        self.assertTrue(isinstance(t.column_descriptors, list))
        self.assertTrue(isinstance(t.column_descriptors[0],
                                   xdata.DimensionDescription))
        print("Test 2: attributes have the correct value")
        self.assertEqual(x.label, 'x')
        self.assertEqual(x.start, 1)
        self.assertEqual(x.scale, 0.5)
        self.assertEqual(x.n_elem, 6)
        self.assertEqual(x.column_descriptors[0].label, 'x')
        self.assertEqual(x.column_descriptors[0].unit, 'mm')
        self.assertEqual(x.column_descriptors[0].dimension_type, 'numeric')

        self.assertEqual(t.label, 'time')
        self.assertEqual(t.start, 0.6)
        self.assertEqual(t.scale, 0.2)
        self.assertEqual(t.n_elem, 100)
        self.assertEqual(t.column_descriptors[0].label, 'time')
        self.assertEqual(t.column_descriptors[0].unit, 's')
        self.assertEqual(t.column_descriptors[0].dimension_type, 'numeric')
        print("Test 3: raising errors for arguments with wrong types")
        self.assertRaises(Exception, xdata.MeasureHeader,
                          t, 0, 100, 0.2, column_descriptors=time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', '0', 100, 0.2, column_descriptors=time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', 0, '100', 0.2, column_descriptors=time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', 0, 100, '0.2', column_descriptors=time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          't', 0, 100, 0.2, column_descriptors=time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 100, 0.2, 's', column_descriptors=time)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, column_descriptors='time')
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, 's', 'ms')
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, check_bank=True)
        self.assertRaises(Exception, xdata.MeasureHeader,
                          'time', 0, 10, 2, 4)
        print("Test 4: testing the __eq__ method")
        self.assertTrue(t == t2)
        self.assertFalse(x == t)
        print("Test 5: testing the __ne__ method")
        self.assertTrue(x != t)
        self.assertFalse(t != t2)
        print("Test 6: testing the get_n_columns method")
        self.assertEqual(x.get_n_columns(), 1)
        print("Test 7: testing the get_units method")
        self.assertEqual(x.get_units(), ['mm'])
        self.assertEqual(t.get_units(), ['s'])
        print("Test 8: testing the get_all_units method")
        self.assertEqual(x.get_all_units(), [[{'unit': 'mm', 'value': 1.0}]])
        self.assertEqual(t.get_all_units(), [[{'unit': 's', 'value': 1.0}]])
        print("Test 9: testing the is_categorical, is_measure, "
              "is_categorical_with_value, and is_undifferentiated")
        self.assertFalse(x.is_categorical)
        self.assertTrue(x.is_measure)
        self.assertFalse(x.is_categorical_with_values)
        self.assertFalse(x.is_undifferentiated)
        print("Test 10: testing the get_value method")
        self.assertEqual(x.get_value(0), 1)
        self.assertEqual(x.get_value(3, 0), 2.5)
        self.assertRaises(Exception, x.get_value, 3, 2)
        self.assertRaises(Exception, x.get_value, 3, -1)
        self.assertRaises(Exception, x.get_value, 'something')
        self.assertRaises(Exception, x.get_value, -10)
        self.assertRaises(Exception, x.get_value, 10)
        print("Test 11: testing the get_item_name method")
        self.assertRaises(Exception, x.get_item_name, 'coffee')
        self.assertRaises(Exception, x.get_item_name, 10)
        self.assertRaises(Exception, x.get_item_name, -10)
        self.assertRaises(Exception, x.get_item_name, ['chocolate', 'milk'])
        self.assertRaises(Exception, x.get_item_name, [10])
        self.assertEqual(x.get_item_name(0), 1)
        self.assertEqual(x.get_item_name([0]), [1])
        self.assertEqual(x.get_item_name([]), [])
        self.assertEqual(x.get_item_name([0, 1, 3, 2]), [1, 1.5, 2.5, 2.0])
        print("Test 12: testing the update_measure_header method")
        self.assertRaises(Exception, x.update_measure_header, 'orange')
        self.assertRaises(Exception, x.update_measure_header, n_elem='apple')
        self.assertRaises(Exception, x.update_measure_header, scale='cherry')
        self.assertEquals(x.update_measure_header(2).label, x.label)
        self.assertEquals(x.update_measure_header(2).start, 2)
        self.assertEquals(x.update_measure_header(n_elem=0).n_elem, 0)
        self.assertEquals(x.update_measure_header(scale=4).scale, 4)
        self.assertEquals(x.update_measure_header(2, 0).scale, 0.5)
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
                          x.update_measure_header(n_elem=30))
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
        x_copy = x.copy()
        x_copy.update_measure_header(4, 5, 1)
        self.assertEqual(x.n_elem, 6)
        self.assertEqual(x.start, 1)
        self.assertEqual(x.scale, 0.5)
        print("\n")

    def test_xdata_module_Xdata_class(self):
        # creating the headers
        time = xdata.DimensionDescription('time', 'numeric', 's')
        t = xdata.MeasureHeader('time',
                                0.6,
                                5,
                                0.2,
                                column_descriptors=time)
        undifferentiated = xdata.CategoricalHeader('repetitions', n_elem=3)
        df_values = pd.DataFrame([['apple', 0.5, 'red'],
                                 ['pear', 0.75, 'green'],
                                 ['banana', 0.66, 'yellow'],
                                 ['cherry', 0.89, 'red']])
        fruits = xdata.CategoricalHeader('fruits',
                                         ['fruits', 'fruit_prices', 'colors'],
                                         4,
                                         df_values)
        # data
        data = np.random.rand(5, 3, 4)

        # the xdata instance
        dataset = xdata.Xdata('name',
                              data,
                              [t, undifferentiated, fruits],
                              'm')
        print("Tests for the class Xdata (module xdata): \n")
        print("Test 1: attributes have the correct type")
        self.assertTrue(isinstance(dataset.name, str))
        self.assertTrue(isinstance(dataset.data, np.ndarray))
        self.assertTrue(isinstance(dataset.headers, list))
        self.assertTrue(isinstance(dataset.headers[1], xdata.Header))
        self.assertTrue(isinstance(dataset.data_descriptor,
                                   xdata.DimensionDescription))
        print("Test 2: attributes have the correct value")
        self.assertEqual(dataset.name, 'name')
        self.assertEqual(dataset.data.shape, data.shape)
        self.assertEqual(dataset.headers[0], t)
        self.assertEqual(dataset.data_descriptor.label, 'name')
        self.assertEqual(dataset.data_descriptor.unit, 'm')
        self.assertEqual(dataset.data_descriptor.dimension_type, 'numeric')
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
        print("Test 4: testing get_n_dimensions method")
        self.assertEqual(dataset.get_n_dimensions(), 3)
        print("Test 5: testing shape method")
        self.assertEqual(dataset.shape(), (5, 3, 4))
        print("Test 6: testing copy method")
        xdata_copy = dataset.copy()
        self.assertEqual(xdata_copy.data_descriptor.all_units,
                         dataset.data_descriptor.all_units)
        series = [pd.Series(['kiwi', 0.95, 'brown']),
                  pd.Series(['blueberry', '1.20', 'blue'])]
        add_fruits = fruits.update_categorical_header('new', None, series)
        slices = [np.random.rand(5, 3), np.random.rand(5, 3)]
        (xdata_copy, flag) = dataset.update_xdata('new',
                                                  2,
                                                  None,
                                                  slices,
                                                  add_fruits)
        self.assertEqual(xdata_copy.shape(), (5, 3, 6))
        self.assertEqual(dataset.shape(), (5, 3, 4))
        self.assertEqual(dataset.headers[2], fruits)
        print("Test 7: testing the update_data method")
        new_data1 = np.random.rand(5, 3, 4)
        ud_dataset1 = dataset.update_data(new_data1)
        new_data2 = np.random.rand(10, 8, 4)
        ud_dataset2 = dataset.update_data(new_data2)
        self.assertEqual(ud_dataset1.get_n_dimensions(), 3)
        self.assertEqual(ud_dataset2.get_n_dimensions(), 3)
        self.assertEqual(ud_dataset1.shape(), (5, 3, 4))
        self.assertEqual(ud_dataset2.shape(), (10, 8, 4))
        self.assertEqual(ud_dataset1.headers[0].n_elem, 5)
        self.assertEqual(ud_dataset2.headers[0].n_elem, 10)
        self.assertEqual(ud_dataset1.headers[1].n_elem, 3)
        self.assertEqual(ud_dataset2.headers[1].n_elem, 8)
        self.assertEqual(ud_dataset1.headers[2].n_elem, 4)
        self.assertEqual(ud_dataset2.headers[2].n_elem, 4)
        self.assertRaises(Exception,
                          dataset.update_data,
                          np.random.rand(5, 3, 4, 5))
        self.assertRaises(Exception,
                          dataset.update_data,
                          np.random.rand(5, 3, 9))
        print("Test 8: testing the update_xdata method")
        # if dim is not an int of out of range, it raises an exception
        new_fruits = fruits.update_categorical_header('chg', [1, 3], series)
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 'yummy', None, new_data1, new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 4, None, new_data1, new_fruits)
        # flag 'all' that should be a 'data_chg' flag (because the header
        # hasn't changed)
        (all_to_chg_data_xdata, flag) = dataset.update_xdata('all',
                                                             1,
                                                             None,
                                                             new_data1,
                                                             undifferentiated)
        self.assertEqual(flag, 'data_chg')
        self.assertEqual(all_to_chg_data_xdata.data[0][0][0], new_data1[0][
            0][0])
        self.assertEqual(dataset.data[0][0][0], data[0][0][0])

        # flag 'all'  (not all exceptions are tested)
        (all_xdata, flag) = dataset.update_xdata('all',
                                                 2,
                                                 None,
                                                 new_data1,
                                                 new_fruits)
        self.assertEqual(flag, 'all')
        self.assertEqual(all_xdata.headers[2].values[0][1], 'kiwi')
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 2, 'yummy', new_data1, new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 2, [1], new_data1, 'yummy')
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 2, [1], 'yummy', new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 2, [1], np.random.rand(5, 3, 4, 2),
                          new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 2, [1], np.random.rand(5, 8, 4), new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'all', 2, [1], np.random.rand(5, 3, 7), new_fruits)
        # flag 'data_chg'
        (data_chg_xdata, flag) = dataset.update_xdata('data_chg',
                                                      1,
                                                      None,
                                                      new_data1,
                                                      None)
        self.assertEqual(flag, 'data_chg')
        self.assertRaises(Exception, dataset.update_xdata,
                          'data_chg', 'yummy', None, new_data1, None)
        self.assertRaises(Exception, dataset.update_xdata,
                          'data_chg', 0, 'yummy', new_data1, None)
        self.assertRaises(Exception, dataset.update_xdata,
                          'data_chg', 0, None, 'yummy', None)
        self.assertRaises(Exception, dataset.update_xdata,
                          'data_chg', 0, None, new_data1, new_fruits)
        # flag 'chg'  (not all exceptions are tested)
        (chg_xdata, flag) = dataset.update_xdata('chg',
                                                 2,
                                                 [1, 3],
                                                 slices,
                                                 new_fruits)
        self.assertEqual(chg_xdata.data[3][0][1], slices[0][3][0])
        self.assertEqual(flag, 'chg')
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 0, [0, 1], slices,
                          xdata.MeasureHeader('time', 0.6, 5, 2,
                                              column_descriptors=time))
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 0, [0, 1], slices, new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 3, [0, 1], slices, t)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 3, 0, slices, new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 3, [0, 1], 'yummy', new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 3, [0, 1, 2], slices, new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 3, [0], [np.random.rand(5, 4)], fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg', 3, [1, 3], slices,
                          fruits.update_categorical_header(
                              'new', None, series))
        # flag 'new'  (not all exceptions are tested)
        add_fruits = fruits.update_categorical_header('new', None, series)
        (new_xdata, flag) = dataset.update_xdata('new',
                                                 2,
                                                 None,
                                                 slices,
                                                 add_fruits)
        self.assertEqual(new_xdata.data[0][0][0], dataset.data[0][0][0])
        self.assertEqual(new_xdata.data[0][0][5], slices[1][0][0])
        self.assertEqual(flag, 'new')
        self.assertEqual(new_xdata.shape(), (5, 3, 6))
        self.assertRaises(Exception, dataset.update_xdata,
                          'new', 0, None, slices, add_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'new', 2, 'yummy', slices, add_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'new', 2, None, slices[0], add_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'new', 2, None, 'yummy', add_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'new', 2, None, slices, 'yummy')
        # flag 'remove' (not all exceptions are tested)
        rm_fruits = fruits.update_categorical_header('remove', [1, 3], None)
        (rm_xdata, flag) = dataset.update_xdata('remove',
                                                2,
                                                [1, 3],
                                                None,
                                                rm_fruits)
        self.assertEqual(flag, 'remove')
        self.assertEqual(rm_xdata.shape(), (5, 3, 2))
        self.assertRaises(Exception, dataset.update_xdata,
                          'remove', 2, [1], None, rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'remove', 0, [1, 3], None, rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'remove', 2, [1, 3], None, 'yummy')
        self.assertRaises(Exception, dataset.update_xdata,
                          'remove', 2, [1, 'yummy'], None, rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'remove', 2, [1, 3], [1, 3], rm_fruits)
        # flag 'chg&new' (not all exceptions are tested)
        chg_and_new_fruits = fruits.update_categorical_header(
            'chg&new', [[0, 1], None], [series, series])
        (chg_and_new_xdata, flag) = dataset.update_xdata(
            'chg&new', 2, [0, 1], [slices, slices], chg_and_new_fruits)
        self.assertEqual(flag, 'chg&new')
        self.assertEqual(chg_and_new_xdata.shape(), (5, 3, 6))
        self.assertEqual(chg_and_new_xdata.data[0][0][5], slices[1][0][0])
        self.assertEqual(chg_and_new_xdata.data[0][0][2],
                         dataset.data[0][0][2])
        self.assertEqual(chg_and_new_xdata.data[0][0][0], slices[0][0][0])
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 1], 'yummy'],
                          [slices, slices], chg_and_new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [],
                          [slices, slices], chg_and_new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 'yummy'], None],
                          [slices, slices], chg_and_new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 1, 3], None],
                          [slices, slices], chg_and_new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [slices], chg_and_new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          'yummy', chg_and_new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [series, slices], chg_and_new_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [slices, slices], fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&new', 2, [[0, 1], None],
                          [slices, slices], 'yummy')
        # flag 'chg&rm' (not all exceptions are tested)
        chg_and_rm_fruits = fruits.update_categorical_header(
            'chg&rm', [[0, 1], [3]], series)
        (chg_and_rm_xdata, flag) = dataset.update_xdata(
            'chg&rm', 2, [[0, 1], [3]], slices, chg_and_rm_fruits)
        self.assertEqual(flag, 'chg&rm')
        self.assertEqual(chg_and_rm_xdata.shape(), (5, 3, 3))
        self.assertEqual(chg_and_rm_xdata.data[0][0][2], dataset.data[0][0][2])
        self.assertEqual(chg_and_rm_xdata.data[0][0][0], slices[0][0][0])
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 'yummy'], [3]],
                          slices, chg_and_rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 1], ['yummy']],
                          slices, chg_and_rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 1]],
                          slices, chg_and_rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 1], [3]],
                          'yummy', chg_and_rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 1], [3]],
                          slices, 'yummy')
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 1, 2], [3]],
                          slices, chg_and_rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 1], [3, 2]],
                          slices, chg_and_rm_fruits)
        self.assertRaises(Exception, dataset.update_xdata,
                          'chg&rm', 2, [[0, 5], [3]],
                          slices, chg_and_rm_fruits)
        # flag 'perm' (not all exceptions are tested)
        (perm_xdata, flag) = dataset.update_xdata('perm',
                                                  2,
                                                  [0, 3, 2, 1],
                                                  None,
                                                  fruits)
        self.assertEqual(flag, 'perm')
        self.assertEqual(perm_xdata.shape(), (5, 3, 4))
        self.assertEqual(perm_xdata.data[2][0][0], dataset.data[2][0][0])
        self.assertEqual(perm_xdata.data[0][0][2], dataset.data[0][0][2])
        self.assertEqual(perm_xdata.data[0][2][1], dataset.data[0][2][3])

        print("Test 9: testing the modify_dimensions method")
        # flag 'global' (not all exceptions are tested)
        (global_xdata, flag) = dataset.modify_dimensions('global',
                                                         None,
                                                         np.random.rand(4, 5),
                                                         [fruits, t])
        self.assertEqual(flag, 'global')
        self.assertEqual(global_xdata.name, dataset.name)
        self.assertEqual(global_xdata.data_descriptor.all_units,
                         dataset.data_descriptor.all_units)
        self.assertEqual(global_xdata.headers[0], fruits)
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'global', 'yummy', np.random.rand(4, 5), [fruits, t])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'global', None, np.random.rand(4, 5), [fruits])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'global', None, 'yummy', [fruits, t])
        # flag 'dim_chg' (not all exceptions are tested)
        header = xdata.CategoricalHeader('label', n_elem=3)
        (dim_chg, flag) = dataset.modify_dimensions('dim_chg',
                                                    [2],
                                                    np.random.rand(5, 3, 3),
                                                    [header])
        self.assertEqual(flag, 'dim_chg')
        self.assertEqual(dim_chg.shape(), (5, 3, 3))
        self.assertEqual(dim_chg.headers[2], header)
        header = header.update_categorical_header('new', None, [pd.Series()])
        self.assertEqual(header.n_elem, 4)
        self.assertEqual(dim_chg.headers[2].n_elem, 3)
        # n_elem of header has been modified from 3 to 4
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_chg', [2], np.random.rand(5, 3, 3), [header])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_chg', [2, 0], np.random.rand(5, 3, 4), [header])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_chg', [2], np.random.rand(5, 3, 4, 3), [header])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_chg', [2], np.random.rand(5, 3, 4), ['yummy'])
        # flag 'dim_insert' (not all exceptions are tested)
        (dim_insert, flag) = dataset.modify_dimensions('dim_insert',
                                                       [1],
                                                       np.random.rand(
                                                           5, 4, 3, 4),
                                                       [header])
        self.assertEqual(flag, 'dim_insert')
        self.assertEqual(dim_insert.shape(), (5, 4, 3, 4))
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_insert', [1], np.random.rand(5, 3, 4, 4),
                          [header])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_insert', 1, np.random.rand(5, 4, 3, 4),
                          [header])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_insert', [1, 2], np.random.rand(5, 4, 3, 4),
                          [header])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_insert', [1], np.random.rand(5, 4, 3, 4, 6),
                          [header])
        # flag 'dim_rm' (not all exceptions are tested)
        (dim_rm, flag) = dataset.modify_dimensions('dim_rm',
                                                   [1],
                                                   np.random.rand(5, 4),
                                                   None)
        self.assertEqual(flag, 'dim_rm')
        self.assertEqual(dim_rm.shape(), (5, 4))
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_rm', [1], np.random.rand(5, 4), [header])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_rm', [1], np.random.rand(5, 4, 2), None)
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_rm', [1, 0], np.random.rand(5, 4), None)
        # flag 'dim_perm' (not all exceptions are tested)
        (dim_perm, flag) = dataset.modify_dimensions('dim_perm',
                                                     [1, 0, 2],
                                                     None,
                                                     None)
        self.assertEqual(flag, 'dim_perm')
        self.assertEqual(dim_perm.shape(), (3, 5, 4))
        self.assertEqual(dim_perm.headers[0], undifferentiated)
        self.assertEqual(dim_perm.headers[1], t)
        self.assertEqual(dim_perm.headers[2], fruits)
        self.assertEqual(dim_perm.data[0][0][0], dataset.data[0][0][0])
        self.assertEqual(dim_perm.data[2][1][3], dataset.data[1][2][3])
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_perm', [0, 0, 0], None, None)
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_perm', [0, 1, 2, 3], None, None)
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_perm', [0, 2, 1], 'yummy', None)
        self.assertRaises(Exception, dataset.modify_dimensions,
                          'dim_perm', [0, 2, 1], np.random.rand(5, 5, 3), None)
        print("\n")

    def test_xdata_module_create_dimension_description_function(self):
        print("Test for the create_dimension_description function \
        (module xdata) \n")
        # checking the Exceptions
        self.assertRaises(Exception, xdata.create_dimension_description, 1, 1)
        self.assertRaises(Exception,
                          xdata.create_dimension_description, 'fruits', 1)
        self.assertRaises(Exception,
                          xdata.create_dimension_description,
                          'fruits',
                          pd.DataFrame([['apple', 0.5],
                                        ['pear', 0.75],
                                        ['banana', 0.66],
                                        ['cherry', 0.89]]))
        # creating DimensionDescription instances with the function
        c = xdata.create_dimension_description('cars')
        fruits = pd.Series(['apple', 'pear', 'banana'])
        f = xdata.create_dimension_description('fruits', fruits)
        mix = pd.Series(['apple', int(3), 'banana'])
        m = xdata.create_dimension_description('mix', mix)
        # creating  DimensionDescription instances without the function
        cdd = xdata.DimensionDescription('cars', 'mixed')
        fdd = xdata.DimensionDescription('fruits', 'string')
        mdd = xdata.DimensionDescription('mix', 'mixed')
        # asserting that both instances are the same
        self.assertEqual(c.label, cdd.label)
        self.assertEqual(c.dimension_type, cdd.dimension_type)
        self.assertEqual(m.label, mdd.label)
        self.assertEqual(m.dimension_type, mdd.dimension_type)
        self.assertEqual(f.label, fdd.label)
        self.assertEqual(f.dimension_type, fdd.dimension_type)


if __name__ == "__main__":
    first_test = MyTestCase()
    first_test.test_xdata_module_DimensionDescription_class()
    first_test.test_xdata_module_CategoricalHeader_class()
    first_test.test_xdata_module_MeasureHeader_class()
    first_test.test_xdata_module_Xdata_class()
    first_test.test_xdata_module_create_dimension_description_function()
