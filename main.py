import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import MenuItem, Reservation, Review, NewsletterSignup

app = FastAPI(title="Restaurant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Restaurant API is running"}

# Menu endpoints
@app.get("/api/menu", response_model=List[MenuItem])
def list_menu(category: Optional[str] = None, featured: Optional[bool] = None):
    try:
        filter_q = {}
        if category:
            filter_q["category"] = category
        if featured is not None:
            filter_q["featured"] = featured
        items = get_documents("menuitem", filter_q)
        # Convert Mongo documents to Pydantic-friendly dicts
        for it in items:
            it.pop("_id", None)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/menu", status_code=201)
def add_menu_item(item: MenuItem):
    try:
        inserted_id = create_document("menuitem", item)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reservation endpoints
@app.get("/api/reservations")
def list_reservations(limit: int = 50):
    try:
        docs = get_documents("reservation", {}, limit=limit)
        for d in docs:
            d["id"] = str(d.pop("_id", ""))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reservations", status_code=201)
def create_reservation(res: Reservation):
    try:
        inserted_id = create_document("reservation", res)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Reviews
@app.get("/api/reviews", response_model=List[Review])
def list_reviews(limit: int = 20):
    try:
        docs = get_documents("review", {}, limit=limit)
        for d in docs:
            d.pop("_id", None)
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reviews", status_code=201)
def create_review(r: Review):
    try:
        inserted_id = create_document("review", r)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Newsletter
@app.post("/api/newsletter", status_code=201)
def newsletter_signup(n: NewsletterSignup):
    try:
        inserted_id = create_document("newslettersignup", n)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health/database test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, "name", "unknown")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
