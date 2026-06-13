import time
from fastapi import Request
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from pydantic import field_validator
from fastapi import FastAPI, HTTPException, Depends, Header
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic_settings import BaseSettings
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 起動時：テーブルを作成
    SQLModel.metadata.create_all(engine)
    print("アプリ起動！")
    yield
    # 終了時（Ctrl+Cのとき）
    print("アプリ終了！")


class Settings(BaseSettings):
    app_name: str = "Default App"
    database_url: str = "sqlite:///database.db"
    secret_key: str = "default-secret"

    class Config:
        env_file = ".env"

settings = Settings()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

@app.get("/settings/")
def read_settings():
    return {"app_name": settings.app_name}

# ベースモデル（共通フィールド）
class HeroBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    age: Optional[int] = Field(default=None, ge=0, le=150)

# DBテーブル（idを持つ）
class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# 入力用（idなし）
class HeroCreate(HeroBase):
    pass

# SQLiteのDB作成（ファイルとして保存される）
engine = create_engine(settings.database_url)


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

@app.patch("/heroes/{hero_id}", response_model=Hero)
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

# 独自例外クラス
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class NotFoundError(AppException):
    def __init__(self, message: str = "リソースが見つかりません"):
        super().__init__(message, status_code=404)

# 例外ハンドラーを登録
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )

# DELETE エンドポイントを書き換え
@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Session = Depends(get_session)):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise NotFoundError("ヒーローが見つかりません")
    session.delete(db_hero)
    session.commit()
    return {"message": "削除しました"}
