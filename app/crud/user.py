from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password
from app import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session,username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def post(db: Session,payload: schemas.UserCreate):   
    db_user = models.User(username=payload.username,email=payload.email,password=get_password_hash(payload.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
  
def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def authenticate_user(db: Session,username: str, password: str)->Optional[models.User]:
    user = get_user(db,username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def put(db: Session,id:int, payload:schemas.UserUpdate):   
    db.query(models.User).filter(models.User.id == id).update({"username":payload.username,"email":payload.email,"password":get_password_hash(payload.password)}, synchronize_session = False)
    db.commit()     
    return get(db,id)  

def delete(db: Session,user_id:int):
    db_data=get(db,user_id)
    db.delete(db_data)     
    db.commit()
    return db_data
    