from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:12345@localhost/blood_bank"

engine = create_engine(DATABASE_URL)