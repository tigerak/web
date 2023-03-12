from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

mysql_url = "sqlite+pysqlite:///:memory:"
engine = create_engine(mysql_url, echo=True)#, convert_unicode=True)

db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))

Base = declarative_base()
Base.query = db_session.query_property()

def init_database(Base):
    Base.metadata.create_all(bind=engine)