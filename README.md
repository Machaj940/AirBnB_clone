First step: Write a command interpreter to manage your AirBnB objects.

This is the first step towards building your first full web application: the AirBnB clone. This first step is very important because you will use what you build during this project with all other following projects: HTML/CSS templating, database storage, API, front-end integration…

Each task is linked and will help you to:

    put in place a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of your future instances
    create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file
    create all classes used for AirBnB (User, State, City, Place…) that inherit from BaseModel
    create the first abstracted storage engine of the project: File storage.
    create all unittests to validate all our classes and storage engine

What’s a command interpreter?

Do you remember the Shell? It’s exactly the same but limited to a specific use-case. In our case, we want to be able to manage the objects of our project:

    Create a new object (ex: a new User or a new Place)
    Retrieve an object from a file, a database etc…
    Do operations on objects (count, compute stats, etc…)
    Update attributes of an object
    Destroy an object


=======================================
STEP 1: WRITING THE BASE CLASS
=======================================

Write a class BaseModel that defines all common attributes/methods for other classes:

    models/base_model.py
    Public instance attributes:
        id: string - assign with an uuid when an instance is created:
            you can use uuid.uuid4() to generate unique id but don’t forget to convert to a string
            the goal is to have unique id for each BaseModel
        created_at: datetime - assign with the current datetime when an instance is created
        updated_at: datetime - assign with the current datetime when an instance is created and it will be updated every time you change your object
    __str__: should print: [<class name>] (<self.id>) <self.__dict__>
    Public instance methods:
        save(self): updates the public instance attribute updated_at with the current datetime
        to_dict(self): returns a dictionary containing all keys/values of __dict__ of the instance:
            by using self.__dict__, only instance attributes set will be returned
            a key __class__ must be added to this dictionary with the class name of the object
            created_at and updated_at must be converted to string object in ISO format:
                format: %Y-%m-%dT%H:%M:%S.%f (ex: 2017-06-14T22:31:03.285259)
                you can use isoformat() of datetime object
            This method will be the first piece of the serialization/deserialization process: create a dictionary representation with “simple object type” of our BaseModel

File: original_base_model.py


=====================================
STEP 2: UPDATING THE BASE CLASS
=====================================

Previously we created a method to generate a dictionary representation of an instance (method to_dict()).

Now it’s time to re-create an instance with this dictionary representation.

<class 'BaseModel'> -> to_dict() -> <class 'dict'> -> <class 'BaseModel'>

Update models/base_model.py:

    __init__(self, *args, **kwargs):
        you will use *args, **kwargs arguments for the constructor of a BaseModel. (more information inside the AirBnB clone concept page)
        *args won’t be used
        if kwargs is not empty:
            each key of this dictionary is an attribute name (Note __class__ from kwargs is the only one that should not be added as an attribute. See the example output, below)
            each value of this dictionary is the value of this attribute name
            Warning: created_at and updated_at are strings in this dictionary, but inside your BaseModel instance is working with datetime object. You have to convert these strings into datetime object. Tip: you know the string format of these datetime
        otherwise:
            create id and created_at as you did previously (new instance)


File: updated_base_model.py



======================================================
STEP 3: SERIALIZE & DESERALIZE TO  AND FROM JSON
======================================================

Now we can recreate a BaseModel from another one by using a dictionary representation:

<class 'BaseModel'> -> to_dict() -> <class 'dict'> -> <class 'BaseModel'>

It’s great but it’s still not persistent: every time you launch the program, you don’t restore all objects created before… The first way you will see here is to save these objects to a file.

Writing the dictionary representation to a file won’t be relevant:

    Python doesn’t know how to convert a string to a dictionary (easily)
    It’s not human readable
    Using this file with another program in Python or other language will be hard.

So, you will convert the dictionary representation to a JSON string. JSON is a standard representation of a data structure. With this format, humans can read and all programming languages have a JSON reader and writer.

Now the flow of serialization-deserialization will be:

<class 'BaseModel'> -> to_dict() -> <class 'dict'> -> JSON dump -> <class 'str'> -> FILE -> <class 'str'> -> JSON load -> <class 'dict'> -> <class 'BaseModel'>

Magic right?

Terms:

    simple Python data structure: Dictionaries, arrays, number and string. ex: { '12': { 'numbers': [1, 2, 3], 'name': "John" } }
    JSON string representation: String representing a simple data structure in JSON format. ex: '{ "12": { "numbers": [1, 2, 3], "name": "John" } }'

Write a class FileStorage that serializes instances to a JSON file and deserializes JSON file to instances:

    models/engine/file_storage.py
    Private class attributes:
        __file_path: string - path to the JSON file (ex: file.json)
        __objects: dictionary - empty but will store all objects by <class name>.id (ex: to store a BaseModel object with id=12121212, the key will be BaseModel.12121212)
    Public instance methods:
        all(self): returns the dictionary __objects
        new(self, obj): sets in __objects the obj with key <obj class name>.id
        save(self): serializes __objects to the JSON file (path: __file_path)
        reload(self): deserializes the JSON file to __objects (only if the JSON file (__file_path) exists ; otherwise, do nothing. If the file doesn’t exist, no exception should be raised)

Update models/__init__.py: to create a unique FileStorage instance for your application

    import file_storage.py
    create the variable storage, an instance of FileStorage
    call reload() method on this variable

Update models/base_model.py: to link your BaseModel to FileStorage by using the variable storage

    import the variable storage
    in the method save(self):
        call save(self) method of storage
    __init__(self, *args, **kwargs):
        if it’s a new instance (not from a dictionary representation), add a call to the method new(self) on storage


Files: models/engine/file_storage.py,
       models/engine/__init__.py,
       models/__init__.py,
       models/base_model.py,
       tests/


=============================================
STEP 4: ENTRY TO THE COMMAND INTERPRETER
=============================================
Write a program called console.py that contains the entry point of the command interpreter:

    You must use the module cmd
    Your class definition must be: class HBNBCommand(cmd.Cmd):
    Your command interpreter should implement:
        quit and EOF to exit the program
        help (this action is provided by default by cmd but you should keep it updated and documented as you work through tasks)
        a custom prompt: (hbnb)
        an empty line + ENTER shouldn’t execute anything
    Your code should not be executed when imported

Warning:

You should end your file with:

if __name__ == '__main__':
    HBNBCommand().cmdloop()

to make your program executable except when imported. Please don’t add anything around - the Checker won’t like it otherwise