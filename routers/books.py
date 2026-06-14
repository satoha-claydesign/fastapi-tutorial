from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, create_engine
from pydantic_settings import BaseSettings
from models import Book, BookCreate
from routers.auth import get_current_user

class Settings(BaseSettings):
    database_url: str = "sqlite:///database.db"
    class Config:
        env_file = ".env"
        extra = "ignore"

engine = create_engine(Settings().database_url)
router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.get("/", response_model=list[Book])
def read_books(session: Session = Depends(get_session)):
    return session.exec(select(Book)).all()

@router.get("/{book_id}", response_model=Book)
def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book)
def create_book(
    book: BookCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),  # 認証必須
):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),  # 認証必須
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": "削除しました"}
