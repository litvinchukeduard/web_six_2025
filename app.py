from src.configuration import engine
from src.models import Author, Book, Genre, book_genre_association_table

from sqlalchemy import text, select, func
from sqlalchemy.orm import Session





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

def get_or_create_genre(book_genre: str, session: Session) -> Genre:
    genre = session.query(Genre).filter_by(name=book_genre).first()
    if not genre:
        genre = Genre(name=book_genre)
        session.add(genre)
        session.flush()
    return genre

def add_genre_to_book(book_id: int, genre_name: str):
    with Session(engine) as session:
        genre = get_or_create_genre(genre_name, session)
        book = session.get(Book, book_id)

        if genre not in book.genres:
            book.genres.append(genre)
            session.commit()

"""
Потрібно взяти автора та вивести кількість книжок по жанру

select g.name, count(g.id) from genres g
join book_genre_association bga on g.id = bga.genre_id
join books b on bga.book_id = b.id
join authors a on b.author_id = a.id
where a.name = 'Daniel Anderson'
group by
	g.id, g.name
"""

def get_genre_statistics(author_name: str):
    with Session(engine) as session:
        sql = (select(Genre, func.count(Genre.id))
            .join(book_genre_association_table, Genre.id == book_genre_association_table.c.genre_id)
            .join(Book, book_genre_association_table.c.book_id == Book.id)
            .join(Author, Book.author_id == Author.id)
            .where(Author.name == author_name)
            .group_by(Genre.id))
        
        return session.execute(sql).all()

def main():

    while True:
        print("Меню:")
        print("1. Додати книгу")
        print("2. Переглянути усі книги")
        print("3. Порахувати кількість книжок")
        print("4. Позначити книгу прочитаною")
        print("5. Видалити автора")
        print("6. Додати жанр до книги")
        print("7. Показати статистику по жанрах")
        print("8. Вийти з додатку")

        choice = int(input("Оберіть дію 1-8: "))

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
            book_id = int(input("Введіть id книги: "))
            genre_name = input("Введіть назву жанру: ")
            add_genre_to_book(book_id, genre_name)

        elif choice == 7:
            author_name = input("Введіть імʼя автора: ")
            print(get_genre_statistics(author_name))
        
        elif choice == 8:
            print("До побачення!")
            break

if __name__ == '__main__':
    main()


