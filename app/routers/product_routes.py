from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional
from .. import models, schemas, auth
from ..database import get_db
from ..crud_helpers import create_item, get_item, update_item, delete_item, list_items

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", dependencies=[Depends(auth.admin_required)])
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    for model, fid, msg in [
        (models.Brand, product.brand_id, "Brand"),
        (models.Category, product.category_id, "Category"),
        (models.SubCategory, product.sub_category_id, "SubCategory")
    ]:
        if not db.query(model).filter(model.id == fid).first():
            raise HTTPException(status_code=404, detail=f"{msg} not found")
    new_product = create_item(db, models.Product, product, unique_field="name")
    return {"message": "Product created successfully", "data": new_product}

@router.get("/")
def list_products(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = Query(None),
    brand_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort_by: str = Query("created_at", regex="^(price|created_at)$"),
    order: str = Query("desc", regex="^(asc|desc)$")
):
    query = db.query(models.Product)
    if category_id: query = query.filter(models.Product.category_id == category_id)
    if brand_id: query = query.filter(models.Product.brand_id == brand_id)
    if min_price is not None: query = query.filter(models.Product.price >= min_price)
    if max_price is not None: query = query.filter(models.Product.price <= max_price)

    sort_column = getattr(models.Product, sort_by)
    query = query.order_by(asc(sort_column) if order == "asc" else desc(sort_column))

    total = query.count()
    products = query.offset((page - 1) * limit).limit(limit).all()

    product_list = [
        schemas.ProductResponse(
            id=p.id, name=p.name, description=p.description, price=p.price, stock=p.stock,
            brand_name=p.brand.name if p.brand else None,
            category_name=p.category.name if p.category else None,
            subcategory_name=p.subcategory.name if p.subcategory else None
        ) for p in products
    ]
    return {"total": total, "page": page, "limit": limit, "products": product_list}

@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = get_item(db, models.Product, product_id)
    return {"message": "Product retrieved successfully", "data": p}

@router.put("/{product_id}", dependencies=[Depends(auth.admin_required)])
def update_product(product_id: int, product_update: schemas.ProductBase, db: Session = Depends(get_db)):
    # Validate foreign keys
    for model, fid, msg in [
        (models.Brand, product_update.brand_id, "Brand"),
        (models.Category, product_update.category_id, "Category"),
        (models.SubCategory, product_update.sub_category_id, "SubCategory")
    ]:
        if not db.query(model).filter(model.id == fid).first():
            raise HTTPException(status_code=404, detail=f"{msg} not found")
    updated_product = update_item(db, models.Product, product_id, product_update, unique_field="name")
    return {"message": "Product updated successfully", "data": updated_product}

@router.delete("/{product_id}", dependencies=[Depends(auth.admin_required)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    delete_item(db, models.Product, product_id)
    return {"message": "Product deleted successfully"}