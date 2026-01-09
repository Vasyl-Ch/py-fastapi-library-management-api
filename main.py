from typing import Generator

from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)
from sqlalchemy.orm import Session

from database import SessionLocal
from schemas import (
    Author,
    AuthorCreate,
    Book,
    BookCreate
)
import crud

app = FastAPI()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/authors/", response_model=list[Author])
def read_authors(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_authors(db, skip=skip, limit=limit)


@app.get("/authors/{author_id}", response_model=Author)
def read_author_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_author_by_id(db, author_id=author_id)


@app.post("/authors/", response_model=Author)
def create_author(
        author: AuthorCreate,
        db: Session = Depends(get_db)
):
    if crud.get_author_by_name(db, author_name=author.name):
        raise HTTPException(
            status_code=400,
            detail="Author already exists"
        )

    return crud.create_author(db, author=author)


@app.get("/books/", response_model=list[Book])
def read_books(
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    return crud.get_all_books(db, skip=skip, limit=limit)


@app.get("/books/{author_id}", response_model=list[Book])
def read_books_by_author_id(
        author_id: int,
        db: Session = Depends(get_db)
):
    return crud.get_all_books(db, author_id=author_id)


@app.post("/books/", response_model=Book)
def create_book(
        book: BookCreate,
        author_id: int,
        db: Session = Depends(get_db)
):
    if crud.get_book_by_title(db, book_title=book.title):
        raise HTTPException(
            status_code=400,
            detail="Book already exists"
        )

    return crud.create_book(db, book=book, author_id=author_id)
