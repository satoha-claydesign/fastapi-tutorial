from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, Header
from sqlmodel import Field, Session, SQLModel, create_engine, select


app = FastAPI()

# ベースモデル（共通フィールド）
class HeroBase(SQLModel):
    name: str
    age: Optional[int] = None

# DBテーブル（idを持つ）
class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# 入力用（idなし）
class HeroCreate(HeroBase):
    pass

# SQLiteのDB作成（ファイルとして保存される）
engine = create_engine("sqlite:///database.db")

# アプリ起動時にテーブルを作成
SQLModel.metadata.create_all(engine)

# DB接続を返す依存関数
def get_session():
    with Session(engine) as session:
        yield session

# ヒーローを作成
# エンドポイントを修正
@app.post("/heroes/", response_model=Hero)
def create_hero(hero: HeroCreate, session: Session = Depends(get_session)):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# ヒーロー一覧を取得
@app.get("/heroes/", response_model=list[Hero])
def read_heroes(session: Session = Depends(get_session)):
    heroes = session.exec(select(Hero)).all()
    return heroes


def verify_token(x_token: str = Header()):
    if x_token != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return x_token

@app.get("/protected/")
def protected_route(token: str = Depends(verify_token)):
    return {"message": "認証成功！", "token": token}

def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/users/")
def read_users(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/books/")
def read_books(commons: dict = Depends(common_parameters)):
    return commons




class ItemCreate(BaseModel):
    name: str
    price: float
    is_available: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    is_available: bool

@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    return {"id": 1, "name": item.name, "price": item.price, "is_available": item.is_available}

fake_db = {1: {"id": 1, "name": "本", "price": 1500.0, "is_available": True}}

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int, q: Optional[str] = None):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

