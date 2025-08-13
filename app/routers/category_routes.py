from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db
from ..crud_helpers import create_item, get_item, update_item, delete_item, list_items

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", dependencies=[Depends(auth.admin_required)])
def create_category(category: schemas.CategoryBase, db: Session = Depends(get_db)):
    new_category = create_item(db, models.Category, category, unique_field="name")
    return {"message": "Category created successfully", "data": new_category}

@router.get("/")
def list_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_items(db, models.Category, skip, limit)

@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    return get_item(db, models.Category, category_id)

@router.put("/{category_id}", dependencies=[Depends(auth.admin_required)])
def update_category(category_id: int, category_update: schemas.CategoryBase, db: Session = Depends(get_db)):
    updated_category = update_item(db, models.Category, category_id, category_update, unique_field="name")
    return {"message": "Category updated successfully", "data": updated_category}

@router.delete("/{category_id}", dependencies=[Depends(auth.admin_required)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    delete_item(db, models.Category, category_id)
    return {"message": "Category deleted successfully"}
