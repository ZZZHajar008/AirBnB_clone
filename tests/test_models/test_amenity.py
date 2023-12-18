#!/usr/bin/python3

"""All the test for the amenity model are implemented"""

import unittest
from models.base_model import BaseModel
from models.amenity import Amenity

class TestAmenity(unittest.TestCase):
    """Testing Amenity class"""

    def test_Amenity_inheritance(self):
        """ tests that the Amenity Inherits from BaseModel"""
        new_amenity = Amenity()
        self.assertIsInstance(new_amenity, BaseModel)

    def test_Amenity_attributes(self):
        """Test that the class of Amenity had a name attribute"""
        new_amenity = Amenity()
        self.assertTrue("name" in new_amenity.__dir__())

    def test_Amenity_attributes_Type(self):
        """Test that Amenity class had a name attribute'type"""
        new_amenity =  Amenity()
        name_value = getattr(new_amenity, "name")
        self.assertIsInstance(name_value, str)
            