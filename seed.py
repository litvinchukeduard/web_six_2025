from src.models import Genre, Book, Author

import random

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from faker import Faker

fake = Faker()

engine = create_engine("postgresql+psycopg://admin:password@localhost:5432/books_db")

GENRES = [
    "Detective",
    "Thriller",
    "Science Fiction",
    "Historical"
]

'''
1. Genres
2. Authors
3. Books
'''

def seed():
    with Session(engine) as session:
        genres = []
        for genre in GENRES:
            genres.append(Genre(name=genre))
        session.add_all(genres)

        authors = []
        for _ in range(7):
            authors.append(Author(name=fake.name()))

        session.add_all(authors)

        session.flush()

        books = []
        for _ in range(30):
            book_author = random.choice(authors)
            book_title = fake.text(50)

            # На кожну книгу нам потрібно 1 до 3 жанрів
            book_genres = random.sample(genres, random.randint(1, 3))

            book = Book(title=book_title, author=book_author, genres=book_genres)

            books.append(book)

        session.add_all(books)
        session.commit()

if __name__ == '__main__':
    seed()
