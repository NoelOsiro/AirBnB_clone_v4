#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        storage = DBStorage()
        self.assertIs(type(storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        storage = DBStorage()
        user_instance = User()
        storage.new(user_instance)
        storage.save()
        result = storage.all()
        self.assertIn(user_instance, result.values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        storage = DBStorage()
        user_instance = User()
        storage.new(user_instance)
        storage.save()
        key = "{}.{}".format(user_instance.__class__.__name__,
        user_instance.id)
        self.assertIn(key, storage.all().keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to the database"""
        storage = DBStorage()
        user_instance = User()
        storage.new(user_instance)
        storage.save()
        key = "{}.{}".format(user_instance.__class__.__name__,
        user_instance.id)
        self.assertIn(key, storage.all().keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test that delete removes an object from the database"""
        storage = DBStorage()
        user_instance = User()
        storage.new(user_instance)
        storage.save()
        key = "{}.{}".format(user_instance.__class__.__name__,
        user_instance.id)
        self.assertIn(key, storage.all().keys())
        storage.delete(user_instance)
        self.assertNotIn(key, storage.all().keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_reload(self):
        """Test that reload loads data from the database"""
        storage = DBStorage()
        user_instance = User()
        storage.new(user_instance)
        storage.save()
        key = "{}.{}".format(user_instance.__class__.__name__,
        user_instance.id)
        self.assertIn(key, storage.all().keys())
        storage.reload()
        self.assertNotIn(key, storage.all().keys())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test the get method of DBStorage"""
        storage = DBStorage()
        user_instance = User()
        storage.new(user_instance)
        storage.save()

        # Test if get returns the correct instance
        retrieved_instance = storage.get(User, user_instance.id)
        self.assertEqual(retrieved_instance, user_instance)

        # Test if get returns None for non-existing instances
        non_existing_instance = storage.get(User, "non-existing-id")
        self.assertIsNone(non_existing_instance)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test the count method of DBStorage"""
        storage = DBStorage()
        user_instance = User()
        city_instance = City()
        amenity_instance = Amenity()

        storage.new(user_instance)
        storage.new(city_instance)
        storage.new(amenity_instance)
        storage.save()

        # Test count for all classes
        total_count = storage.count()
        self.assertEqual(total_count, 3)

        # Test count for a specific class
        user_count = storage.count(User)
        self.assertEqual(user_count, 1)

        city_count = storage.count(City)
        self.assertEqual(city_count, 1)

        amenity_count = storage.count(Amenity)
        self.assertEqual(amenity_count, 1)

        # Test count for a non-existing class
        non_existing_count = storage.count(Place)
        self.assertEqual(non_existing_count, 0)
