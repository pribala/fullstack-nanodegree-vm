import sys

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


# class for defining category info
class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), primary_key=True)
    # id = Column(Integer, primary_key=True)
    # We added this serialize function to be able to send JSON objects in a
    # serializable format

    @property
    def serialize(self):

        return {
            'name': self.name
        }


# class for defining user info
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


# class for defining item info
class Item(Base):
    __tablename__ = 'item'
    title = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    time_created = Column(DateTime, default=func.current_timestamp())
    last_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())  # noqa
    category_id = Column(Integer, ForeignKey('category.name'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

# We added this serialize function to be able to send JSON objects in a
# serializable format
    @property
    def serialize(self):

        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }

engine = create_engine('sqlite:///itemcatalog.db')
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
