from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email is required")
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    role: str = Field("User", description="Role defaults to User")

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email is required")
    password: str = Field(..., description="Password is required")

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class BrandBase(BaseModel):
    name: str
    description: Optional[str] = None

    @validator("name")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Field cannot be empty")
        return v

class BrandResponse(BrandBase):
    id: int

    class Config:
        from_attributes = True


from pydantic import BaseModel, Field, validator
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., description="Category name is required")
    description: Optional[str] = None

    @validator("name")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Category name cannot be empty")
        return v

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class SubCategoryBase(BaseModel):
    name: str = Field(..., description="Subcategory name is required")
    description: Optional[str] = None
    category_id: int = Field(..., gt=0, description="Parent category id is required and must be >0")

    @validator("name")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Subcategory name cannot be empty")
        return v

class SubCategoryResponse(SubCategoryBase):
    id: int
    category: CategoryResponse

    class Config:
        from_attributes = True

from pydantic import BaseModel, Field, validator

class ProductBase(BaseModel):
    name: str = Field(..., description="Product name is required")
    description: str = Field(..., description="Product description is required")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    stock: int = Field(..., ge=0, description="Stock must be 0 or more")
    brand_id: int = Field(..., gt=0, description="Brand ID is required and must be >0")
    category_id: int = Field(..., gt=0, description="Category ID is required and must be >0")
    sub_category_id: int = Field(..., gt=0, description="SubCategory ID is required and must be >0")

    @validator("name")
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Product name cannot be empty")
        return v

    @validator("description")
    def description_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Product description cannot be empty")
        return v

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    brand_name: str
    category_name: str
    subcategory_name: str

    class Config:
        from_attributes = True
