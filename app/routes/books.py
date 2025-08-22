from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas
from ..deps import get_db

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookResponse, status_code=201)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == book.owner_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_book = models.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=List[schemas.BookWithOwner])
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Book).offset(skip).limit(limit).all()


@router.get("/{book_id}", response_model=schemas.BookWithOwner)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.BookResponse)
async def update_book(
    book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_update.owner_id and book_update.owner_id != book.owner_id:
        owner = (
            db.query(models.User).filter(models.User.id == book_update.owner_id).first()
        )
        if not owner:
            raise HTTPException(status_code=404, detail="New owner not found")

    for field, value in book_update.dict(exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


@router.get("/search/", response_model=List[schemas.BookWithOwner])
async def search_books(
    title: Optional[str] = None,
    author: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Book.author.ilike(f"%{author}%"))
    return query.offset(skip).limit(limit).all()
