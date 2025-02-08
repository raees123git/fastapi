from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
# sqlalchemy is use to create a database, and help the server to connect with database.

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# print(Base)



# 🔹 Why Do We Need Base?
# It registers all models (tables) in a central place.
# It allows SQLAlchemy to track and map Python classes to database tables.
# It helps create and update database tables automatically.
