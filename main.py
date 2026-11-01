import os

import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("The DATABASE_URL environment variable is not set.")

app = FastAPI()


class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None


def get_connection():
    """Open a new database connection. Rows are returned as dictionaries."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@app.get("/books", response_model=list[Book])
def get_books():
    with get_connection() as conn:
        books = conn.execute(
            "SELECT id, title, author, year FROM books ORDER BY id"
        ).fetchall()
    return books


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    with get_connection() as conn:
        book = conn.execute(
            "SELECT id, title, author, year FROM books WHERE id = %s",
            (book_id,),
        ).fetchone()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.post("/books", response_model=Book, status_code=201)
def create_book(book_data: BookCreate):
    with get_connection() as conn:
        new_book = conn.execute(
            """
            INSERT INTO books (title, author, year)
            VALUES (%s, %s, %s)
            RETURNING id, title, author, year
            """,
            (book_data.title, book_data.author, book_data.year),
        ).fetchone()
    return new_book


@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookUpdate):
    with get_connection() as conn:
        updated_book = conn.execute(
            """
            UPDATE books
            SET title  = COALESCE(%s::text, title),
                author = COALESCE(%s::text, author),
                year   = COALESCE(%s::integer, year)
            WHERE id = %s
            RETURNING id, title, author, year
            """,
            (book_data.title, book_data.author, book_data.year, book_id),
        ).fetchone()

    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    with get_connection() as conn:
        result = conn.execute("DELETE FROM books WHERE id = %s", (book_id,))
        deleted_count = result.rowcount

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
