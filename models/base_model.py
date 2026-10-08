#!/usr/bin/python3
"""
Module containing the BaseModel class.
"""

import uuid
from datetime import datetime
import models


class BaseModel:
    """
    Base class for other classes in the project.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel.

        Args:
            args: Additional positional arguments (unused).
            kwargs: Additional keyword arguments for initialization.
        """

        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key == "created_at" or key == "updated_at":
                    setattr(self, key, datetime.strptime(value, time_format))
                else:
                    setattr(self, key, value)

        models.storage.new(self)

    def save(self):
        """
        Updates the 'updated_at' attribute and saves the instance to storage.
        """
        self.updated_at = datetime.now()

        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the instance.

        Returns:
            dict: Dictionary representation of the instance.
        """
        ins_dict = self.__dict__.copy()
        ins_dict["__class__"] = self.__class__.__name__
        ins_dict["created_at"] = self.created_at.isoformat()
        ins_dict["updated_at"] = self.updated_at.isoformat()
        return ins_dict

    def __str__(self):
        """
        Returns a string representation of the instance.

        Returns:
            str: String representation of the instance.
        """
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)
