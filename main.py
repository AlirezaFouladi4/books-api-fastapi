from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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


books: dict[int, Book] = {
    1: Book(id=1, title="Clean Code", author="Robert C. Martin", year=2008),
    2: Book(id=2, title="The Pragmatic Programmer", author="Andrew Hunt and David Thomas", year=1999),
    3: Book(id=3, title="Fluent Python", author="Luciano Ramalho", year=2015),
}

next_id = len(books) + 1


@app.get("/books", response_model=list[Book])
def get_books():
    return list(books.values())


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]


@app.post("/books", response_model=Book, status_code=201)
def create_book(book_data: BookCreate):
    global next_id

    new_book = Book(
        id=next_id,
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
    )
    books[next_id] = new_book
    next_id += 1
    return new_book


@app.patch("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    changes = book_data.model_dump(exclude_none=True)
    updated_book = books[book_id].model_copy(update=changes)
    books[book_id] = updated_book
    return updated_book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")

    del books[book_id]
