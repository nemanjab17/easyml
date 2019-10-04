from sqlalchemy import Column, Integer, String
from database.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    password = Column(String(120), unique=False)

    def __repr__(self):
        return '<User %r>' % self.name