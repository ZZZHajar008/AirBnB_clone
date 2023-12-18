#!/usr/bin/python3
"""
All the test for the user model are implemented here
"""

import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.city import City


class TestUser(unittest.TestCase):
    """Testing User class"""

    def test_City_inheritance(self):
        """tests that the City class Inherits from BaseModel"""
        new_city = City()
        self.assertIsInstance(new_city, BaseModel)

    def test_User_attributes(self):
        new_city = City()
        self.assertTrue("state_id" in new_city.__dir__())
        self.assertTrue("name" in new_city.__dir__())

    def test_type_name(self):
        """Test the type of name"""
        new_city = City()
        name = getattr(new_city, "name")
        self.assertIsInstance(name, str)

    def test_type_name(self):
        """Test the type of name"""
        new_city = City()
        name = getattr(new_city, "state_id")
        self.assertIsInstance(name, str)

    def setUp(self):
        """Setup the unit tests"""
        self.obj1 = City()
        self.obj2 = City()
        self.obj3 = City()
        self.obj4 = City()
        self.obj11 = City(**self.obj1.to_dict())
        self.obj22 = City(**self.obj2.to_dict())
        self.obj33 = City(**self.obj3.to_dict())

    def test_init(self):
        """Test initialization without kwargs"""
        self.assertIsInstance(self.obj1.id, str)
        self.assertIsInstance(self.obj1.created_at, datetime)
        self.assertIsInstance(self.obj1.updated_at, datetime)
        self.assertNotEqual(self.obj1.id, self.obj2.id)
        self.assertNotEqual(self.obj3.id, self.obj4.id)
        self.assertEqual(self.obj1.__class__.__name__, "City")

    def test_id_uniqueness(self):
        """Check if id is always universal unique"""
        alot_of_ids = [City().id for i in range(1000)]
        self.assertEqual(len(set(alot_of_ids)), 1000)

    def test_types(self):
        """Test the properties types"""
        self.assertIsInstance(self.obj1, City)
        self.assertIsInstance(self.obj11, City)
        self.assertIsInstance(self.obj33.id, str)

    def test_init_kwargs(self):
        """Test initialization with kwargs"""
        self.assertIsInstance(self.obj11.id, str)
        self.assertIsInstance(self.obj11.created_at, datetime)
        self.assertIsInstance(self.obj11.updated_at, datetime)
        self.assertEqual(self.obj2.id, self.obj22.id)
        self.assertEqual(self.obj3.updated_at, self.obj33.updated_at)
        self.assertEqual(self.obj3.created_at, self.obj33.created_at)
        self.assertEqual(self.obj11.__class__.__name__, "City")

    def test_init_args(self):
        """The case where args are given"""
        args = [i for i in range(20)]
        obj = City(*args)
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.to_dict(), dict)

    def test_to_dict(self):
        """Test the to_dict method"""
        returned_dict = self.obj2.to_dict()
        self.assertEqual(returned_dict["__class__"], "City")
        self.assertIsInstance(returned_dict["created_at"], str)
        self.assertIsInstance(returned_dict["updated_at"], str)
        self.assertEqual(len(self.obj22.to_dict()), 4)
        self.assertIsInstance(returned_dict, dict)
        self.assertDictEqual(self.obj33.to_dict(), self.obj33.to_dict())

    def test_save(self):
        """Test the save method"""
        before_save = self.obj1.updated_at
        before_save_create = self.obj1.created_at
        self.obj1.save()
        after_save_create = self.obj1.created_at
        after_save = self.obj1.updated_at
        self.assertNotEqual(before_save, after_save)
        self.assertEqual(before_save_create, after_save_create)

    def test_str(self):
        """Test the str method"""
        format_str = (self.obj1.id, self.obj1.__dict__)
        str_rep = "[City] ({}) {}".format(*format_str)
        self.assertEqual(str_rep, str(self.obj1))
        format_str = (self.obj2.id, self.obj2.__dict__)
        str_rep = "[City] ({}) {}".format(*format_str)
        self.assertEqual(str_rep, str(self.obj2))
