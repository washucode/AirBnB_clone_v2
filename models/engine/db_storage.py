#!/usr/bin/python3
"""
This module defines a class to manage db storage for hbnb clone
"""

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
    }


class DBStorage:
    """ uses SQLAlchemy to store data """
    __engine = None
    __session = None

    def __init__(self):
        """ creates the engine """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'dev':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns a dictionary of all objects """
        if cls is None:
            objs = []
            for clss in classes.values():
                objs += self.__session.query(clss).all()
        else:
            objs = self.__session.query(cls).all()
        return {"{}.{}".format(type(obj).__name__, obj.id):
                obj for obj in objs}

    def new(self, obj):
        """ adds a new object """
        self.__session.add(obj)

    def save(self):
        """ commits changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ deletes an object """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ reloads data """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def classes(self):
        """ returns a dictionary of classes """
        return classes

    def close(self):
        """ closes the session """
        self.__session.close()
