from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://admin:password@localhost:5432/books_db")

