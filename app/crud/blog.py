from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app import models, schemas


def post(db: Session,payload: schemas.BlogCreate):   
    db_query = models.Blog(title=payload.title,description=payload.description,owner_id=payload.owner_id)
    db.add(db_query)
    db.commit()
    db.refresh(db_query)
    return db_query


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()

def get(db: Session, id: int):
    return db.query(models.Blog).filter(models.Blog.id == id).first()


def put(db: Session,id: int, payload=schemas.BlogUpdate):
    db.query(models.Blog).filter(models.Blog.id == id).update({"title":payload.title,"title":payload.title,"owner_id":payload.owner_id},synchronize_session=False) 
    db.commit()         
    return get(db,id)  

def delete(db: Session,id: int):
    db_data=get(db,id)
    db.delete(db_data)  
    db.commit()    
    return db_data
    