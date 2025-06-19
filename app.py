from configuration import engine

from sqlalchemy import ForeignKey, String, Boolean, select, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


'''
Book (id: int, title: str, author: str, is_read: bool)
'''


class Base(DeclarativeBase):
    pass


'''
Author -> Book

Assumption: One book has one author

ManyToOne
'''


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship(cascade="all, delete-orphan")

    def __str__(self):
        # return f'Author({self.id}, {self.name}, {self.books})'
        return f'Author({self.id}, {self.name})'


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Author] = relationship()

    def __str__(self):
        return f'Book({self.id}, {self.title}, {self.author})'
    


'''
Написати бота для керування книжками

1
2
3
4
'''

def get_or_create_author(book_author: str, session: Session) -> Author:
    author = session.query(Author).filter_by(name=book_author).first()
    if not author:
        author = Author(name=book_author)
        session.add(author)
        session.flush()
    return author

def add_book(book_title: str, book_author: str):
    with Session(engine) as session:
        author = get_or_create_author(book_author, session)
        book = Book(title=book_title, author=author)
        
        session.add(book)
        session.commit()
        print(f"Книгу '{book.title}' збережено")

def delete_author(author_id: int):
    with Session(engine) as session:
        author = session.get(Author, author_id)
        if not author:
            print('Немає автора')
            return
        session.delete(author)
        session.commit()
        print(f'Автор {author.id}. {author.name} був видалений')

def list_all_books():
    with Session(engine) as session:
        books = session.query(Book).all()
        for book in books:
            print(book)

def count_all_books() -> int:
    with engine.connect() as connection:
        # SELECT count(*) from books;
        # count_query = select(Book, func.count(Book.id))
        count_query = text("select count(id) from books")
        result = connection.execute(count_query)
        return result.scalar_one()

def mark_book_as_read(book_id: int):
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if not book:
            print('Книгу не знайдено!')
            return
        book.is_read = True
        session.commit()

def main():

    while True:
        print("Меню:")
        print("1. Додати книгу")
        print("2. Переглянути усі книги")
        print("3. Порахувати кількість книжок")
        print("4. Позначити книгу прочитаною")
        print("5. Видалити автора")
        print("6. Вийти з додатку")

        choice = int(input("Оберіть дію 1-6: "))

        if choice == 1:
            title = input("Введіть назву книги:")
            author = input("Введіть імʼя автора книги:")
            add_book(title, author)

        elif choice == 2:
            list_all_books()

        elif choice == 3:
            print(f'Кількість книжок {count_all_books()}')

        elif choice == 4:
            book_id = int(input("Введіть id книги: "))
            mark_book_as_read(book_id)

        elif choice == 5:
            author_id = int(input("Введіть id автора: "))
            delete_author(author_id)
        
        elif choice == 6:
            print("До побачення!")
            break

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    main()


