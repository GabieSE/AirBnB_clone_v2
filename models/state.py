#!/usr/bin/python3
"""
Module containing the State class, which inherits from BaseModel.
"""

from models.base_model import BaseModel


class State(BaseModel):
    """
    Represents a state, inheriting from the BaseModel.

    Attributes:
        name (str): The name of the state.
    """
    name = ""
