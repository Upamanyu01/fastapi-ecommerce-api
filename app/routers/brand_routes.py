from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db
from ..crud_helpers import create_item, get_item, update_item, delete_item, list_items

router = APIRouter(prefix="/brands", tags=["Brands"])

@router.post("/", dependencies=[Depends(auth.admin_required)])
def create_brand(brand: schemas.BrandBase, db: Session = Depends(get_db)):
    new_brand = create_item(db, models.Brand, brand, unique_field="name")
    return {"message": "Brand created successfully", "data": new_brand}

@router.get("/")
def list_brands(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return list_items(db, models.Brand, skip, limit)

@router.get("/{brand_id}")
def get_brand(brand_id: int, db: Session = Depends(get_db)):
    return get_item(db, models.Brand, brand_id)

@router.put("/{brand_id}", dependencies=[Depends(auth.admin_required)])
def update_brand(brand_id: int, brand_update: schemas.BrandBase, db: Session = Depends(get_db)):
    updated_brand = update_item(db, models.Brand, brand_id, brand_update, unique_field="name")
    return {"message": "Brand updated successfully", "data": updated_brand}

@router.delete("/{brand_id}", dependencies=[Depends(auth.admin_required)])
def delete_brand(brand_id: int, db: Session = Depends(get_db)):
    delete_item(db, models.Brand, brand_id)
    return {"message": "Brand deleted successfully"}
