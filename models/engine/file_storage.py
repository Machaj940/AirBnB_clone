#!/usr/bin/python3
'''
    Define class FileStorage
'''
import json


class FileStorage:
    '''
        Serializes instances to JSON file and deserializes to JSON file
        to instances.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self):
        '''return the dictionary'''
        return FileStorage.__objects

    def new(self, obj):
        '''set in __objects the obj with key <obj class name>.id'''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''serializes __objects attribute to JSON file.'''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''deserializes the JSON file to __objects.'''
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                FileStorage.__objects[key] = eval(class_name)(**val)
        except FileNotFoundError:
            pass
