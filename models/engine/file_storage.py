#!/usr/bin/python3
"""Serialize and deserialize objects to and from a JSON file."""

import json
import os


class FileStorage:
    """Stores objects in a JSON file."""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Return all objects, or only those of the given class."""
        if cls is None:
            return FileStorage.__objects
        return {k: v for k, v in FileStorage.__objects.items()
                if isinstance(v, cls)}

    def new(self, obj):
        """Add obj to the objects dictionary."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Write all objects to the JSON file."""
        obj_dict = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Load objects from the JSON file, if it exists."""
        from models.base_model import BaseModel
        from models.user import User
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.place import Place
        from models.review import Review
        classes = {"BaseModel": BaseModel, "User": User, "State": State,
                   "City": City, "Amenity": Amenity, "Place": Place,
                   "Review": Review}

        if not os.path.isfile(FileStorage.__file_path):
            return
        with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
            try:
                obj_dict = json.load(f)
            except json.JSONDecodeError:
                return
        for key, value in obj_dict.items():
            cls = classes[value["__class__"]]
            FileStorage.__objects[key] = cls(**value)

    def delete(self, obj=None):
        """Delete obj from storage if it exists."""
        if obj is None:
            return
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects.pop(key, None)

    def get(self, cls, id):
        """Return one object by class and id, or None."""
        if cls is None or id is None:
            return None
        return FileStorage.__objects.get("{}.{}".format(cls.__name__, id))

    def count(self, cls=None):
        """Count all objects, or those of one class."""
        return len(self.all(cls))

    def close(self):
        """Reload from file (used by the API teardown)."""
        self.reload()