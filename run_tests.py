#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys
import unittest

from tests.favourites_test import FavouritesTestCase
from tests.slider_test import SliderTestCase


if __name__ == '__main__':
    suite = unittest.TestSuite((
        # unittest.makeSuite(FavouritesTestCase),
        unittest.makeSuite(SliderTestCase),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
