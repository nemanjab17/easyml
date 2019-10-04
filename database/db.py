from sqlalchemy.ext.declarative import declarative_base
DB_URI = "postgresql+psycopg2://nemanja:admin@localhost:5432/easyml"
Base = declarative_base()