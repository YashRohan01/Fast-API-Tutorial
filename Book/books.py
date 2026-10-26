from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'},
    {'title': 'Another Title Four', 'author': 'Author Four', 'category': 'math'}
]

@app.get("/")
async def home_page():
    return {'message': "Hello World"}


@app.get("/api-endpoint")
async def first_api():
    return {'message': 'Hello Yash'}

@app.get("/books")
async def get_all_books():
    return BOOKS


@app.get("/books/title/{book_title}")
async def get_book_by_title(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book
    return {'message': 'Book not found'}

@app.get("/books/category/")
async def get_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/author/{book_author}/")
async def get_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book = Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
            return {'message': 'Book updated successfully'}
    return {'message': 'Book not found'}

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            BOOKS.remove(book)
            return {'message': 'Book deleted successfully'}
    return {'message': 'Book not found'}

#Assignment 1: Create a new endpoint to get all books from a specific author using path or query parameters.
@app.get("/books/author_all/{author_name}")
async def get_book_by_author_name(author_name: str):
    all_books = []
    for book in BOOKS:
        if book.get('author').casefold() == author_name.casefold():
            all_books.append(book)
    return all_books