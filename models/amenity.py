#!/usr/bin/python3
"""A module that contains Amenity class
"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity, inheriting from the BaseModel.

    Attributes:
        name (str): The name of the amenity.

    Note:
        This class inherits common attributes and methods from the BaseModel.
    """
    name = ""
