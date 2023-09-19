#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
      'BaseModel': BaseModel,
      'User': User,
      'Place': Place,
      'State': State,
      'City': City,
      'Amenity': Amenity,
      'Review': Review
      }


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'

    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if (not cls):
            return {key: obj for key, obj in self.__objects.items()
                    if isinstance(obj, cls)}
        else:
            return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        json_objects = {key: obj.to_dict() for key, obj
                        in self.__objects.items()}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                json_objects = json.load(f)
            for key, val in json_objects.items():
                class_name = val['__class__']
                if class_name in classes:
                    objects = classes[class_name](**val)
                    self.__objects[key] = objects
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from __object if it exists"""
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """Calls reload method to deserialize JSON file to objects"""
        self.reload()
