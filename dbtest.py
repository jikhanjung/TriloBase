import os

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, LargeBinary, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import LONGBLOB
import mysql.connector

Base = declarative_base()

class Box(Base):
    __tablename__ = 'box'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))


class Sample(Base):
    __tablename__ = 'sample'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    box_id = Column(Integer, ForeignKey('box.id'))
    box = relationship(
        Box,
        backref=backref('samples',
                         uselist=True,
                         cascade='delete,all'))

class ScientificName(Base):
    __tablename__= 'scientificname'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))

class Specimen(Base):
    __tablename__ = 'specimen'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    sample_id = Column(Integer, ForeignKey('sample.id'))
    scientificname_id = Column(Integer, ForeignKey('scientificname.id'))
    photo = Column(LargeBinary().with_variant(LONGBLOB, "mysql"))
    sample = relationship(
        Sample,
        backref=backref('specimens',
                         uselist=True,
                         cascade='delete,all'))
    scientificname = relationship(
        ScientificName,
        backref=backref('specimens',
                         uselist=True,
                         cascade='delete,all'))

from sqlalchemy import create_engine

#engine = create_engine('sqlite:///trilobase.sqlite')
engine = create_engine("mysql+mysqlconnector://root:2volutio@localhost/trilobase")

from sqlalchemy.orm import sessionmaker

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)