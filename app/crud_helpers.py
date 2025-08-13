from fastapi import HTTPException
from sqlalchemy.orm import Session

def create_item(db: Session, model, data, unique_field: str = None):
    if unique_field:
        exists = db.query(model).filter(getattr(model, unique_field) == getattr(data, unique_field)).first()
        if exists:
            raise HTTPException(status_code=400, detail=f"{model.__name__} already exists")
    new_item = model(**data.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_item(db: Session, model, item_id: int):
    item = db.query(model).filter(model.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return item

def update_item(db: Session, model, item_id: int, data, unique_field: str = None):
    item = get_item(db, model, item_id)
    if unique_field:
        exists = db.query(model).filter(getattr(model, unique_field) == getattr(data, unique_field),
                                        model.id != item_id).first()
        if exists:
            raise HTTPException(status_code=400, detail=f"{model.__name__} {unique_field} already in use")
    for key, value in data.dict().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_item(db: Session, model, item_id: int):
    item = get_item(db, model, item_id)
    db.delete(item)
    db.commit()
    return True

def list_items(db: Session, model, skip: int = 0, limit: int = 10):
    total = db.query(model).count()
    items = db.query(model).offset(skip).limit(limit).all()
    return {"total": total, "skip": skip, "limit": limit, "data": items}
