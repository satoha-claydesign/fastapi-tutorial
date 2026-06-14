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
from routers import heroes, auth
from models import Hero, HeroBase, HeroCreate

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

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(heroes.router, prefix="/heroes", tags=["heroes"])

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


# SQLiteのDB作成（ファイルとして保存される）
engine = create_engine(settings.database_url)


# DB接続を返す依存関数
def get_session():
    with Session(engine) as session:
        yield session

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

