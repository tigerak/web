from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from make_data.init_db import Base

class para_data(Base):
    __tablename__='para_data'
    
    id = Column(Integer, primary_key=True)
    para = Column(String, unique=True)
    
    def __init__(self, para):
        self.para = para
        
    def __repr__(self):
        return f'{self.para}'
    
class sent_data(Base):
    __tablename__='sent_data'
    
    id = Column(Integer, primary_key=True)
    
    
    def __repr__(self):
        return 'sssssssssssss'