from fastapi import FastAPI, Body, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app =FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

    def __init__(self, id, title, author, description, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_year = published_year

class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str= Field(min_length=3, max_length=1000)
    rating: int = Field(gt=-1, lt=6)
    published_year:int = Field(description="Year when the Book got published", gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example":{
                "title": "A new Book",
                "author": "Author Name",
                "description": "describe the book",
                "rating": 5,
                "published_year": 2026
            }
        }
    }

BOOKS = [
    Book(1, 'Intro to Fast API', 'Yash', 'Good book for understanding', 5,2026),
    Book(2, 'Intro to Math', 'Rhea', 'Very great Mathematician', 5, 2025),
    Book(3, 'Intro to DBs', 'Anku', 'Very Hard to understand', 2, 2024),
    Book(4, 'Intro to Taxation', 'Arun', 'Very okay book', 3, 2026),
    Book(5, 'Intro to Teaching', 'Anita', 'Very Bad', 1, 2022),
    Book(6, '6th Book', 'Author 6', 'Test', 0, 2021),
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

"""
@app.post("/create_book")
async def create_book(book_request = Body()):
    BOOKS.append(book_request)
"""
"""
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    BOOKS.append(book_request)
"""

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    """    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    """
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item Not Found")

@app.get("/books/rating/")
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

@app.get("/books/published_year/")
async def read_book_by_year(published_year: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_year == published_year:
            books_to_return.append(book)
    return books_to_return

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item Not Found")

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message":"Deleted Succesfully"}
    return {"message": "book id could not be matched"}

