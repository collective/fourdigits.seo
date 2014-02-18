import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import ketomatic.contenttypes

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['ketomatic.contenttypes'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              ketomatic.contenttypes)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='ketomatic.contenttypes',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='ketomatic.contenttypes.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='ketomatic.contenttypes',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for IngredientFolder
        ztc.ZopeDocFileSuite(
            'IngredientFolder.txt',
            package='ketomatic.contenttypes',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for RecipeFolder
        ztc.ZopeDocFileSuite(
            'RecipeFolder.txt',
            package='ketomatic.contenttypes',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Ingredient
        ztc.ZopeDocFileSuite(
            'Ingredient.txt',
            package='ketomatic.contenttypes',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for Recipe
        ztc.ZopeDocFileSuite(
            'Recipe.txt',
            package='ketomatic.contenttypes',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
