#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from models.base_model import Base
from os import getenv
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import unittest
import models


class DBStorage:
    """This class manages storage of hbnb models in a database"""

    __engine = None
    __session = None

    def __init__(self):
        """ Creates a new instance """
        str_conn = 'mysql+mysqldb://{}:{}@{}/{}'\
            .format(getenv('HBNB_MYSQL_USER'),
                    getenv('HBNB_MYSQL_PWD'),
                    getenv('HBNB_MYSQL_HOST'),
                    getenv('HBNB_MYSQL_DB'))
        self.__engine = create_engine(str_conn, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Queries a database for objects """
        if not cls:
            res_list = self.__session.query(Amenity)
            res_list.extend(self.__session.query(City))
            res_list.extend(self.__session.query(Place))
            res_list.extend(self.__session.query(Review))
            res_list.extend(self.__session.query(State))
            res_list.extend(self.__session.query(User))
        else:
            res_list = res_list = self.__session.query(cls)
        return {'{}.{}'.format(type(obj).__name__, obj.id): obj
                for obj in res_list}

    def new(self, obj):
        """ Adds an objet to the current db session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes 'obj' from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Handles db and session creation """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close method"""
        self.__session.close()
