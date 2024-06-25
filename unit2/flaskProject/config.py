from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI =  'postgresql://postgres:1234@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
