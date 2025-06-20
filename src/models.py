from sqlalchemy import ForeignKey, String, Boolean, Table, Column
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

book_genre_association_table = Table(
    "book_genre_association",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("genre_id", ForeignKey("genres.id"), primary_key=True),
)

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)

    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    author: Mapped[Author] = relationship()

    genres: Mapped[list["Genre"]] = relationship(secondary=book_genre_association_table)

    def __str__(self):
        return f'Book({self.id}, {self.title}, {self.author})'

'''
Genre -> Book

ManyToMany

(1, 1)
(1, 2)
(2, 1)
'''




class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    # books: Mapped[list[Book]] = relationship(
    #     secondary=book_genre_association_table, back_populates="genres"
    # )
    def __str__(self):
        return f'Genre({self.id}, {self.name})'
    
    def __repr__(self):
        return str(self)
    
