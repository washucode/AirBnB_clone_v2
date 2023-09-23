#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


# Test not relevant for db storage
@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                 'not relevant'
                 )
class test_basemodel(unittest.TestCase):
    """ Test cases for the BaseModel class """
    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ Set up testing environment """
        pass

    def tearDown(self):
        """ Remove testing environment """
        try:
            os.remove('file.json')
        except Exception:
            pass

    def test_default(self):
        """ Test default creation of BaseModel """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """
        Test creation of BaseModel with invalid keyword
        arguments (int keys)
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_kwargs_int(self):
        """
        Test creation of BaseModel with invalid keyword arguments (int keys)
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ Test the __str__ method of BaseModel """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ Test the to_dict method of BaseModel """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """
        Test creation of BaseModel with invalid keyword
        arguments (None values)
        """
        n = {None: None}
        with self.assertRaises(TypeError) as context:
            new = self.value(**n)
        # Check that the expected error message contains the
        # string "keywords must be strings"
        self.assertIn("keywords must be strings", str(context.exception))

    def test_kwargs_one(self):
        """
        Test creation of BaseModel with invalid keyword
        arguments (single key not 'Name'
        """
        n = {'Name': 'test'}
        new = self.value(**n)
        self.assertEqual(new.Name, 'test')

    def test_id(self):
        """ Test the type of the id attribute """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ Test the type of the created_at attribute """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ Test the type of the updated_at attribute """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)
