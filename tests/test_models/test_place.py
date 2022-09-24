#!/usr/bin/python3
"""User test"""
from datetime import datetime
import inspect
import models
import pep8 as pycodestyle
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
import time
import unittest
from unittest import mock
Model = models.place.Place
Place = models.place.Place
module_doc = models.place.__doc__
path1 = "models/place.py"
path2 = "tests/test_models/test_place.py"


class DocsTest(unittest.TestCase):
    """Test to check behaviors"""

    @classmethod
    def setUpClass(self):
        """setting up tests"""
        self.self_funcs = inspect.getmembers(Model, inspect.isfunction)

    def test_pep8(self):
        """Testing pep8"""
        for path in [path1,
                     path2]:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test module docstring"""
        self.assertIsNot(module_doc, None,
                         "place.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "test_place.py needs a docstring")

        """Test classes doctring"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "Place class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) >= 1,
                        "Place class needs a docstring")

    def test_func_docstrings(self):
        """test func dostrings"""
        for func in self.self_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


@unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
class TestBaseModel(unittest.TestCase):
    """testing BaseModel Class"""
    @mock.patch('models.place')
    def test_instances(self, mock_storage):
        """Testing that object is correctly created"""
        instance = Place()
        self.assertIs(type(instance), Place)
        instance.name = "Holbies foravaaaa"
        instance.description = "really nice"
        instance.number_rooms = 2
        instance.number_bathrooms = 3
        instance.max_guest = 4
        instance.price_by_night = 30
        instance.latitude = 2.5
        instance.longitude = 5.4
        instance.longitude = 5.4
        instance.amenity_ids = ["11", "22"]

        expectec_attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "description": str,
            "number_rooms": int,
            "number_bathrooms": int,
            "max_guest": int,
            "price_by_night": int,
            "latitude": float,
            "longitude": float,
            "amenity_ids": list
        }

        # testing types and attr names
        for attr, types in expectec_attrs_types.items():
            with self.subTest(attr=attr, typ=types):
                self.assertIn(attr, instance.__dict__)
                self.assertIs(type(instance.__dict__[attr]), types)
        self.assertEqual(instance.name, "Holbies foravaaaa")
        self.assertEqual(instance.description, "really nice")
        self.assertEqual(instance.number_rooms, 2)
        self.assertEqual(instance.number_bathrooms, 3)
        self.assertEqual(instance.max_guest, 4)
        self.assertEqual(instance.price_by_night, 30)
        self.assertEqual(instance.latitude, 2.5)
        self.assertEqual(instance.longitude, 5.4)
        self.assertEqual(instance.amenity_ids, ['11', '22'])

    def test_datetime(self):
        """testing correct datetime assignation
        correct assignation of created_at and updated_at"""
        created_at = datetime.now()
        instance1 = Place()
        updated_at = datetime.now()
        self.assertEqual(created_at <= instance1.created_at <=
                         updated_at, True)
        time.sleep(0.1)
        created_at = datetime.now()
        instance2 = Place()
        updated_at = datetime.now()
        self.assertTrue(created_at <= instance2.created_at <= updated_at, True)
        self.assertEqual(instance1.created_at, instance1.created_at)
        self.assertEqual(instance2.updated_at, instance2.updated_at)
        self.assertNotEqual(instance1.created_at, instance2.created_at)
        self.assertNotEqual(instance1.updated_at, instance2.updated_at)

    def test_uuid(self):
        """testing uuid"""
        instance1 = Place()
        instance2 = Place()
        for instance in [instance1, instance2]:
            tuuid = instance.id
            with self.subTest(uuid=tuuid):
                self.assertIs(type(tuuid), str)

    def test_dictionary(self):
        """testing to_dict correct funtionality"""
        """Testing that object is correctly created"""
        instance3 = Place()
        self.assertIs(type(instance3), Place)
        instance3.name = "Holbies foravaaaa"
        new_inst = instance3.to_dict()
        expectec_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "__class__"]
        self.assertCountEqual(new_inst.keys(), expectec_attrs)
        self.assertEqual(new_inst['__class__'], 'Place')
        self.assertEqual(new_inst['name'], 'Holbies foravaaaa')

    def test_str_method(self):
        """testing str method, checking output"""
        instance4 = Place()
        strr = "[Place] ({}) {}".format(instance4.id, instance4.__dict__)
        self.assertEqual(strr, str(instance4))

    @mock.patch('models.storage')
    def test_save_method(self, mock_storage):
        """test save method and if it updates
        "updated_at" calling storage.save"""
        instance4 = Place()
        created_at = instance4.created_at
        updated_at = instance4.updated_at
        instance4.save()
        new_created_at = instance4.created_at
        new_updated_at = instance4.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)
