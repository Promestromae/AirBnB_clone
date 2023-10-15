#!/usr/bin/python3

""" Define the FileStorage class. """
import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    A class to handle serialization and deserialization
    of objects to/from JSON format.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary of objects.

        Returns:
            dict: A dictionary containing objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the __objects dictionary.

        Args:
            obj (BaseModel): The object to be added.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes objects to JSON and saves them to the file.
        """
        data = {}
        for key, value in FileStorage.__objects.items():
            data[key] = value.to_dict()
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as f:
            json.dump(data, f)

    def reload(self):
        """
        Deserializes JSON data from the file and creates objects.
        """
        try:
            with open(FileStorage.__file_path) as fl:
                obj_dict = json.load(fl)
                for val in obj_dict.values():
                    c_name = val["__class__"]
                    del val["__class__"]
                    self.new(eval(c_name)(**val))
        except FileNotFoundError:
            return
