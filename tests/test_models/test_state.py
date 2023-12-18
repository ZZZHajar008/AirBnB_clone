#!/usr/bin/python3

"""Contain tests for the state module"""
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.state import State


class TestState(unittest.TestCase):
    """Test the State class"""

    def test_State_inheritence(self):
        """Testing the state class that contains the attribute 'name'"""
        new_state = State()
        self.assertIsInstance(new_state, BaseModel)

    def test_State_attributes(self):
        """Test the class State which contains the attributes 'name'"""
        new_state = State()
        self.assertTrue("name" in new_state.__dir__())

    def test_State_attributes_type(self):
        """ Test the State class in which attribute
        name is the class type str"""
        new_state = State()
        name = getattr(new_state, "name")
        self.assertIsInstance(name, str)

    def setUp(self):
        """Setup the unit tests"""
        self.obj1 = State()
        self.obj2 = State()
        self.obj3 = State()
        self.obj4 = State()
        self.obj11 = State(**self.obj1.to_dict())
        self.obj22 = State(**self.obj2.to_dict())
        self.obj33 = State(**self.obj3.to_dict())

    def test_init(self):
        """Test initialization without kwargs"""
        self.assertIsInstance(self.obj1.id, str)
        self.assertIsInstance(self.obj1.created_at, datetime)
        self.assertIsInstance(self.obj1.updated_at, datetime)
        self.assertNotEqual(self.obj1.id, self.obj2.id)
        self.assertNotEqual(self.obj3.id, self.obj4.id)
        self.assertEqual(self.obj1.__class__.__name__, "State")

    def test_id_uniqueness(self):
        """Check if id is always universal unique"""
        alot_of_ids = [State().id for i in range(1000)]
        self.assertEqual(len(set(alot_of_ids)), 1000)

    def test_types(self):
        """Test the properties types"""
        self.assertIsInstance(self.obj1, State)
        self.assertIsInstance(self.obj11, State)
        self.assertIsInstance(self.obj33.id, str)

    def test_init_kwargs(self):
        """Test initialization with kwargs"""
        self.assertIsInstance(self.obj11.id, str)
        self.assertIsInstance(self.obj11.created_at, datetime)
        self.assertIsInstance(self.obj11.updated_at, datetime)
        self.assertEqual(self.obj2.id, self.obj22.id)
        self.assertEqual(self.obj3.updated_at, self.obj33.updated_at)
        self.assertEqual(self.obj3.created_at, self.obj33.created_at)
        self.assertEqual(self.obj11.__class__.__name__, "State")

    def test_init_args(self):
        """The case where args are given"""
        args = [i for i in range(20)]
        obj = State(*args)
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.to_dict(), dict)

    def test_to_dict(self):
        """Test the to_dict method"""
        returned_dict = self.obj2.to_dict()
        self.assertEqual(returned_dict["__class__"], "State")
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
        str_rep = "[State] ({}) {}".format(*format_str)
        self.assertEqual(str_rep, str(self.obj1))
        format_str = (self.obj2.id, self.obj2.__dict__)
        str_rep = "[State] ({}) {}".format(*format_str)
        self.assertEqual(str_rep, str(self.obj2))
