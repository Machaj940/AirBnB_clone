#!/usr/bin/python3
"""Class User inherits from BaseModel"""


from models.base_model import BaseModel


class User(BaseModel):
    """the User class"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
