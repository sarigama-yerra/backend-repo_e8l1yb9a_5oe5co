from database import create_document, get_documents, db
from schemas import MenuItem

sample_items = [
    {
        "name": "Burrata Caprese",
        "description": "Creamy burrata with heirloom tomatoes, basil, and balsamic glaze",
        "price": 14.0,
        "category": "Starters",
        "image": "https://images.unsplash.com/photo-1604908177093-4a3f2e0d1b7f?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": False,
        "is_gluten_free": True,
        "is_spicy": False,
        "featured": True,
    },
    {
        "name": "Truffle Fries",
        "description": "Hand-cut fries tossed in truffle oil, parmesan, and herbs",
        "price": 9.0,
        "category": "Starters",
        "image": "https://images.unsplash.com/photo-1550547660-d9450f859349?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": False,
        "is_gluten_free": False,
        "is_spicy": False,
        "featured": False,
    },
    {
        "name": "Wood-Fired Margherita Pizza",
        "description": "San Marzano tomatoes, fior di latte, fresh basil",
        "price": 18.0,
        "category": "Mains",
        "image": "https://images.unsplash.com/photo-1542281286-9e0a16bb7366?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": False,
        "is_gluten_free": False,
        "is_spicy": False,
        "featured": True,
    },
    {
        "name": "Wild Mushroom Risotto",
        "description": "Arborio rice, seasonal mushrooms, pecorino, herb oil",
        "price": 22.0,
        "category": "Mains",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": False,
        "is_gluten_free": True,
        "is_spicy": False,
        "featured": False,
    },
    {
        "name": "Spicy Ahi Tuna Bowl",
        "description": "Sushi-grade tuna, jasmine rice, avocado, sesame, chili mayo",
        "price": 20.0,
        "category": "Mains",
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": False,
        "is_gluten_free": True,
        "is_spicy": True,
        "featured": False,
    },
    {
        "name": "Vegan Chocolate Torte",
        "description": "Rich dark chocolate, almond crust, sea salt",
        "price": 11.0,
        "category": "Desserts",
        "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476a?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": True,
        "is_gluten_free": True,
        "is_spicy": False,
        "featured": False,
    },
    {
        "name": "Classic Tiramisu",
        "description": "Espresso-soaked ladyfingers, mascarpone, cocoa",
        "price": 10.0,
        "category": "Desserts",
        "image": "https://images.unsplash.com/photo-1601979031925-424e53b6caaa?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": False,
        "is_gluten_free": False,
        "is_spicy": False,
        "featured": True,
    },
    {
        "name": "Elderflower Spritz",
        "description": "Elderflower liqueur, prosecco, soda, citrus",
        "price": 12.0,
        "category": "Drinks",
        "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": True,
        "is_gluten_free": True,
        "is_spicy": False,
        "featured": False,
    },
    {
        "name": "Spiced Chai Latte",
        "description": "House-made chai, steamed milk, warm spices",
        "price": 6.0,
        "category": "Drinks",
        "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?q=80&w=1200&auto=format&fit=crop",
        "is_vegan": True,
        "is_gluten_free": True,
        "is_spicy": False,
        "featured": False,
    },
]

def upsert_menu():
    if db is None:
        raise SystemExit("Database not configured. Set DATABASE_URL and DATABASE_NAME.")

    existing = {doc.get("name"): doc for doc in get_documents("menuitem", {})}
    inserted, skipped = 0, 0
    for item in sample_items:
        if item["name"] in existing:
            skipped += 1
            continue
        mi = MenuItem(**item)
        create_document("menuitem", mi)
        inserted += 1
    print(f"Menu seeding complete. inserted={inserted}, skipped={skipped}")

if __name__ == "__main__":
    upsert_menu()
