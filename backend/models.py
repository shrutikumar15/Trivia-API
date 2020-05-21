import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.exc import SQLAlchemyError

database_name = "trivia"
password = 'root'
user = 'shrut'
database_path = "postgres://{}:{}@{}/{}".format(user, password,'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    try:
      app.config["SQLALCHEMY_DATABASE_URI"] = database_path
      app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
      db.app = app
      db.init_app(app)
      db.create_all()
      print("Database connected")
    except SQLAlchemyError as e:
      print("Database not connected")  
      print(e)

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    try:
      db.session.add(self)
      db.session.commit()
      print("insert successful")
    except SQLAlchemyError as e:
      print("insert not successful")  
      print(e)
    
  
  def update(self):
    db.session.commit()

  def delete(self):
    try:
      db.session.delete(self)
      db.session.commit()
      print("delete successful")
    except SQLAlchemyError as e:
      print("delete not successful")  
      print(e)
    

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }