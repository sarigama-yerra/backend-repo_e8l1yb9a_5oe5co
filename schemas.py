"""
Database Schemas for the Restaurant app

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase class name (e.g., MenuItem -> "menuitem").
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Core domain schemas
class MenuItem(BaseModel):
    name: str = Field(..., description="Dish name")
    description: Optional[str] = Field(None, description="Short description of the dish")
    price: float = Field(..., ge=0, description="Price in USD")
    category: str = Field(..., description="Category like Starters, Mains, Desserts, Drinks")
    image: Optional[str] = Field(None, description="Image URL")
    is_vegan: bool = Field(False)
    is_spicy: bool = Field(False)
    is_gluten_free: bool = Field(False)
    featured: bool = Field(False, description="Showcase on hero/featured section")

class Reservation(BaseModel):
    name: str = Field(..., description="Guest full name")
    email: EmailStr
    phone: Optional[str] = Field(None)
    date: str = Field(..., description="ISO date string (YYYY-MM-DD)")
    time: str = Field(..., description="24h time string (HH:MM)")
    party_size: int = Field(..., ge=1, le=20)
    notes: Optional[str] = None
    occasion: Optional[str] = Field(None, description="Birthday, Anniversary, Business, etc.")

class Review(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    date: Optional[datetime] = Field(default_factory=datetime.utcnow)

# Example additional schemas users can expand later
class NewsletterSignup(BaseModel):
    email: EmailStr

