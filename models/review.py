#!/usr/bin/python3
"""
Module containing the Review class, which inherits from BaseModel.
"""

from models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review, inheriting from the BaseModel.

    Attributes:
        place_id (str): The ID of the place associated with the review.
        user_id (str): The ID of the user who created the review.
        text (str): The text content of the review.
    """

    place_id = ""

    user_id = ""

    text = ""
