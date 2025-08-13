from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db
from ..crud_helpers import create_item, get_item, update_item, delete_item, list_items

router = APIRouter(prefix="/subcategories", tags=["SubCategories"])

@router.post("/", dependencies=[Depends(auth.admin_required)])
def create_subcategory(subcategory: schemas.SubCategoryBase, db: Session = Depends(get_db)):
    if not db.query(models.Category).filter(models.Category.id == subcategory.category_id).first():
        raise HTTPException(status_code=404, detail="Parent category not found")
    new_subcategory = create_item(db, models.SubCategory, subcategory, unique_field="name")
    return {"message": "SubCategory created successfully", "data": new_subcategory}

@router.get("/")
def list_subcategories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_items(db, models.SubCategory, skip, limit)

@router.get("/{subcategory_id}")
def get_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    return get_item(db, models.SubCategory, subcategory_id)

@router.put("/{subcategory_id}", dependencies=[Depends(auth.admin_required)])
def update_subcategory(subcategory_id: int, subcategory_update: schemas.SubCategoryBase, db: Session = Depends(get_db)):
    if not db.query(models.Category).filter(models.Category.id == subcategory_update.category_id).first():
        raise HTTPException(status_code=404, detail="Parent category not found")
    updated_subcategory = update_item(db, models.SubCategory, subcategory_id, subcategory_update, unique_field="name")
    return {"message": "SubCategory updated successfully", "data": updated_subcategory}

@router.delete("/{subcategory_id}", dependencies=[Depends(auth.admin_required)])
def delete_subcategory(subcategory_id: int, db: Session = Depends(get_db)):
    delete_item(db, models.SubCategory, subcategory_id)
    return {"message": "SubCategory deleted successfully"}
