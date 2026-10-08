#!/usr/bin/python3
"""
Module containing the City class, which inherits from BaseModel.
"""

from models.base_model import BaseModel


class City(BaseModel):
    """
     Represents a city, inheriting from the BaseModel.

    Attributes:
        state_id (str): The ID of the state to which the city belongs.
        name (str): The name of the city.
    """
    state_id = ""

    name = ""
