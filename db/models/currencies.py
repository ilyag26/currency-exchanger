from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class currency(Base):
    _tablename_ = 'Currencies'
    id = Column(Integer(), primary_key=True, unique = True)
    Code = Column(String(50), unique = True)
    FullName = Column(String(50))
    Sign = Column(String(50))

    def __str__(self):
        return self.username

