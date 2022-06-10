from typing import Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends, Request,APIRouter,Path
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel

from app.api import deps
from app.crud import user
from app import schemas

router = APIRouter()

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"  
    authjwt_decode_algorithms: set = {"HS384","HS512"}

@AuthJWT.load_config
def get_config():
    return Settings()

@router.post("/login")
def login(payload: schemas.UserLogin,Authorize: AuthJWT = Depends(),db: Session = Depends(deps.get_db)):
    user_data=user.authenticate_user(db,payload.username, payload.password)    
    if not user_data:
        raise HTTPException(status_code=401,detail="Bad username or password")
    
    access_token = Authorize.create_access_token(subject=user_data.username,algorithm="HS384")
    refresh_token = Authorize.create_refresh_token(subject=user_data.username,algorithm="HS512")
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/me/", response_model=schemas.User)
def read_users_me(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

@router.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user,algorithm="HS384")
    return {"access_token": new_access_token}

@router.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

@router.post("/", response_model=schemas.User, status_code=201)
def create_user(payload: schemas.UserCreate,db: Session = Depends(deps.get_db)):   
    db_user = user.get_user_by_email(db, email=payload.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user.post(db,payload)    
    
    
@router.get("/{id}/", response_model=schemas.User)
def read_user(id: int = Path(..., gt=0),db: Session = Depends(deps.get_db)):
    user_data = user.get(db,id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.get("/", response_model=List[schemas.User])
def read_all_users(skip: int = 0, limit: int = 100, db: Session = Depends(deps.get_db)):
    return user.get_all(db, skip=skip, limit=limit)

@router.put("/{id}/", response_model=schemas.User)
def update_user(payload:schemas.UserUpdate,id:int=Path(...,gt=0),db: Session = Depends(deps.get_db)):
    user_data = user.get(db,id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")   
    return user.put(db,id,payload)

#DELETE route
@router.delete("/{id}/", response_model=schemas.User)
def delete_user(id:int = Path(...,gt=0),db: Session = Depends(deps.get_db)):
    user_data = user.get(db,id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")       
    return user.delete(db,id) 
