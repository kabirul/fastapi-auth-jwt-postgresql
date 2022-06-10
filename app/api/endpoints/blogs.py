from typing import Any, List
from fastapi import Depends,APIRouter, HTTPException, Path, FastAPI
from sqlalchemy.orm import Session
from app.api import deps

from app.crud import blog
from app import schemas

router = APIRouter()


@router.post("/", response_model=schemas.Blog, status_code=201)
def create_blog(payload: schemas.BlogCreate,db: Session = Depends(deps.get_db)):
    return blog.post(db,payload)   
    
@router.get("/{id}/", response_model=schemas.Blog)
def read_blog(id: int = Path(..., gt=0),db: Session = Depends(deps.get_db)):
    blog_data = blog.get(db,id)
    if not blog_data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog_data

@router.get("/", response_model=List[schemas.Blog])
def read_all_blogs(skip: int = 0, limit: int = 100,db: Session = Depends(deps.get_db)):
    return blog.get_all(db, skip=skip, limit=limit)

@router.put("/{id}/", response_model=schemas.Blog)
def update_blog(payload:schemas.BlogUpdate,id:int=Path(...,gt=0),db: Session = Depends(deps.get_db)): 
    blog_data = blog.get(db,id)
    if not blog_data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog.put(db,id,payload)
   

#DELETE route
@router.delete("/{id}/", response_model=schemas.Blog)
def delete_blog(id:int = Path(...,gt=0),db: Session = Depends(deps.get_db)):
    blog_data = blog.get(db,id)
    if not blog_data:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog.delete(db,id)
