#!/usr/bin/python3

"""

Test the file storage mechanism

"""

import json
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test the file storage module"""

    @classmethod
    def setUpClass(cls):
        """Set up the class"""
        path = FileStorage._FileStorage__file_path
        with open(path, "w") as f:
            f.write("{}")

    def reset_file(self):
        """Function to rest file"""
        with open(self.path, "w") as f:
            f.write("{}")
        self.file_content = {}
        self.engine.reload()

    def read_file(self):
        """Read conetent of a file"""
        with open(self.path, "r") as f:
            self.file_content = json.load(f)

    def setUp(self):
        """Write into file ewo instances"""
        self.path = FileStorage._FileStorage__file_path
        self.engine = FileStorage()
        self.obj = BaseModel()
        self.obj.save()
        self.read_file()

    def tearDown(self):
        """Empty the file after every test"""
        self.reset_file()

    def test_all_1(self):
        """Test if the path exist"""
        self.tearDown()
        self.assertEqual(self.file_content, {})
        self.assertEqual(self.engine.all(), {})

    def test_save(self):
        """Test the save mothod"""
        file_key = list(self.file_content.keys())[0]
        file_dict = self.file_content[file_key]
        engine_dict = self.engine.all()[file_key]

        key = f"BaseModel.{self.obj.id}"
        self.assertEqual(file_key, key)
        self.assertIsInstance(file_dict, dict)
        self.assertEqual(file_dict["__class__"], "BaseModel")
        self.assertIsInstance(file_dict["__class__"], str)
        self.assertIsInstance(file_dict["updated_at"], str)
        self.assertIsInstance(file_dict["id"], str)
        self.assertIsInstance(engine_dict.id, str)
        self.assertIsInstance(engine_dict.updated_at, datetime)
        self.assertIsInstance(engine_dict.created_at, datetime)

    def test_all_2(self):
        """Test the all method"""
        self.reset_file()
        number_inct = 120
        for i in range(0, number_inct):
            BaseModel()
        self.engine.save()
        self.read_file()
        self.assertEqual(len(self.file_content), number_inct)
        self.assertEqual(len(self.engine.all()), number_inct)
        keys = self.file_content.keys()
        id_test = [i.startswith("BaseModel.") for i in keys]
        self.assertTrue(all(id_test))

    def help_test_all_classes(self, classname):
        """Helper tests all() method with many objects for classname."""

        cls = self.engine.types[classname]
        objs = [cls() for i in range(1000)]
        self.assertEqual(len(objs), len(self.engine.all()))
        for o in objs:
            key = "{}.{}".format(type(o).__name__, o.id)
            self.assertTrue(key in self.engine.all())
            self.assertEqual(self.engine.all()[key], o)

    def test_base_model(self):
        """Test storage with base model class"""
        self.reset_file()
        self.help_test_all_classes("BaseModel")

    def test_city(self):
        """Test storage with City class"""
        self.reset_file()
        self.help_test_all_classes("City")

    def test_place(self):
        """Test storage with place class"""
        self.reset_file()
        self.help_test_all_classes("Place")

    def test_review(self):
        """Test storage with Review class"""
        self.reset_file()
        self.help_test_all_classes("Review")

    def test_amenity(self):
        """Test storage with Amenity class"""
        self.reset_file()
        self.help_test_all_classes("Amenity")

    def test_user(self):
        """Test storage with User class"""
        self.reset_file()
        self.help_test_all_classes("User")

    def test_state(self):
        """Test storage with State class"""
        self.reset_file()
        self.help_test_all_classes("State")
