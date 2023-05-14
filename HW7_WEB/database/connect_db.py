from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:0987654321@0.0.0.0:5432')
Session = sessionmaker(bind=engine)
session = Session()