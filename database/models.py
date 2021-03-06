from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from database.db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=False)
    email = Column(String(120), unique=True)
    password = Column(String(120), unique=False)

    def __repr__(self):
        return '<User %r>' % self.name


class FileRecord(Base):
    __tablename__ = 'files'
    id = Column(String(40), primary_key=True)
    filename = Column(String(50), unique=False)
    content_type = Column(String(50), unique=False)
    header = Column(JSON, unique=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<File %r>' % self.filename

    def as_dict(self, cols=None):
        result = {}
        for c in self.__table__.columns:
            if cols:
                if c.name in cols:
                    result[c.name] = getattr(self, c.name)
            else:
                result[c.name] = getattr(self, c.name)
        return result
