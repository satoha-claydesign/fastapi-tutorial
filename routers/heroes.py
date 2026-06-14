from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, create_engine
from pydantic_settings import BaseSettings
from models import Hero, HeroCreate

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

@router.post("/", response_model=Hero)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.get("/", response_model=list[Hero])
def read_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes

@router.patch("/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    db_hero.sqlmodel_update(hero_data)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router.delete("/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(db_hero)
    session.commit()
    return {"message": "削除しました"}