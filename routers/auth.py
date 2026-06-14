from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth import verify_password, create_access_token, decode_token, get_password_hash

router = APIRouter()

# 仮のユーザーDB（本来はDBから取得）
fake_users_db = {
    "user@example.com": {
        "email": "user@example.com",
        "hashed_password": get_password_hash("password123"),
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="メールアドレスまたはパスワードが違います")
    token = create_access_token(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    email = decode_token(token)
    if not email or email not in fake_users_db:
        raise HTTPException(status_code=401, detail="認証が必要です")
    return fake_users_db[email]

@router.get("/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["email"]}
