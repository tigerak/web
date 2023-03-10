from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from make_data.init_db import db_session

class train_data(Base):
    __tablename__='train_data'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    sent: Mapped[str] = mapped_column(String(300))
    