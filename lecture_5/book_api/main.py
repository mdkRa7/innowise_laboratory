from fastapi import FastAPI, HTTPException, Depends, Query, status
from sqlalchemy import create_engine, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, sessionmaker
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
import uvicorn

# ============================================
# 1. DATABASE SETUP (SQLAlchemy 2.0)
# ============================================

SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base class with SQLAlchemy 2.0 syntax
class Base(DeclarativeBase):
    pass


# ============================================
# 2. DATABASE MODEL (SQLAlchemy 2.0)
# ============================================

class BookDB(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


Base.metadata.create_all(bind=engine)


# ============================================
# 3. PYDANTIC SCHEMAS (Pydantic v2 - modern syntax)
# ============================================

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1000, le=2100)

    # New validator syntax in Pydantic v2
    @field_validator('year')
    @classmethod
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 1000 or v > 2100):
            raise ValueError('Year must be between 1000 and 2100')
        return v


class BookCreate(BookBase):
    pass


class BookResponse(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ============================================
# 4. DEPENDENCIES
# ============================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================
# 5. FASTAPI APPLICATION
# ============================================

app = FastAPI(
    title="Book Collection API",
    description="API for managing book collection",
    version="1.0.0"
)


# ============================================
# 6. ENDPOINTS (EXACTLY 5 AS PER REQUIREMENTS)
# ============================================

@app.post("/books/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Add a new book"""
    db_book = BookDB(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/", response_model=List[BookResponse])
def read_books(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        db: Session = Depends(get_db)
):
    """Get all books with pagination"""
    books = db.query(BookDB).offset(skip).limit(limit).all()
    return books


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book by ID"""
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    db.delete(db_book)
    db.commit()
    return None


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookCreate, db: Session = Depends(get_db)):
    """Update book details"""
    db_book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    # Update fields using model_dump()
    for field, value in book_update.model_dump().items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books/search/", response_model=List[BookResponse])
def search_books(
        title: Optional[str] = Query(None),
        author: Optional[str] = Query(None),
        year: Optional[int] = Query(None, ge=1000, le=2100),
        db: Session = Depends(get_db)
):
    """Search books by title, author, or year"""
    query = db.query(BookDB)
    if title:
        query = query.filter(BookDB.title.contains(title))
    if author:
        query = query.filter(BookDB.author.contains(author))
    if year:
        query = query.filter(BookDB.year == year)
    return query.all()


@app.get("/")
def read_root():
    return {
        "message": "Book Collection API is running!",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": [
            "POST /books/ - Add a book",
            "GET /books/ - Get all books",
            "DELETE /books/{id} - Delete a book",
            "PUT /books/{id} - Update a book",
            "GET /books/search/ - Search books"
        ]
    }


# ============================================
# 7. RUN APPLICATION
# ============================================

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)