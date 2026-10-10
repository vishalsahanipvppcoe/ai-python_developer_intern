from datetime import timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.database.session import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.services.user import create_user, authenticate_user
from app.auth.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    return create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login to get an access token."""
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def read_users_me(current_user: User = Depends(get_current_user)):
    """Get the current authenticated user."""
    return current_user
