#!/usr/bin/python3
"""
Handles serialization and deserialization of objects to and from a JSON file.
"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models.city import City


class FileStorage:
    """
    Handles serialization and deserialization of
    objects to and from a JSON file.
    """
    __file_path = "file.json"

    __objects = {}

    def all(self):
        """
        Returns the dictionary __objects.

        Returns:
            dict: The dictionary containing all serialized objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the __objects dictionary.

        Args:
            obj: The object to be added to the dictionary.
        """
        obj_cls_name = obj.__class__.__name__

        key = "{}.{}".format(obj_cls_name, obj.id)

        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes the objects in __objects and saves them to a JSON file.
        """
        all_objs = FileStorage.__objects

        obj_dict = {}

        for obj in all_objs.keys():
            obj_dict[obj] = all_objs[obj].to_dict()

        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """
        Deserializes objects from the JSON file and updates __objects.
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                try:
                    obj_dict = json.load(f)

                    for key, value in obj_dict.items():
                        class_name, obj_id = key.split('.')

                        cls = eval(class_name)

                        instance = cls(**values)

                        FileStorage.__objects[key] = instance
                except Exception:
                    pass
