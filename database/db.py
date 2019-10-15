import os
from sqlalchemy.ext.declarative import declarative_base

DATABASE = {
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "NAME": os.environ["POSTGRES_DB"],
        "PORT": os.environ["POSTGRES_PORT"],
    }

DB_URI = f"postgresql+psycopg2://{DATABASE.get('USER')}:{DATABASE.get('PASSWORD')}@{DATABASE.get('HOST')}:{DATABASE.get('PORT')}/{DATABASE.get('NAME')}"
Base = declarative_base()