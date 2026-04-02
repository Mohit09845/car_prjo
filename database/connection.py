import os
from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["car_db"]

car_collection = db["cars"]
variant_collection = db["variants"]


def get_db():
    return db


def ensure_indexes():
    # ── cars ──────────────────────────────────────────────────────────────────
    # Unique: prevent duplicate car entries
    car_collection.create_index(
        [("make", ASCENDING), ("model", ASCENDING)],
        unique=True,
        name="idx_cars_make_model_unique",
    )
    # Filter / sort by car type (Hatchback, Sedan …)
    car_collection.create_index(
        [("type", ASCENDING)],
        name="idx_cars_type",
    )

    # ── variants ──────────────────────────────────────────────────────────────
    # Unique: prevent duplicate variant names within the same car
    variant_collection.create_index(
        [("car_id", ASCENDING), ("name", ASCENDING)],
        unique=True,
        name="idx_variants_car_id_name_unique",
    )
    # Most common query: "get all variants for car X"
    variant_collection.create_index(
        [("car_id", ASCENDING)],
        name="idx_variants_car_id",
    )
    # Filter by fuel type (Petrol / CNG)
    variant_collection.create_index(
        [("fuel", ASCENDING)],
        name="idx_variants_fuel",
    )
    # Filter by transmission (Manual / AMT)
    variant_collection.create_index(
        [("transmission", ASCENDING)],
        name="idx_variants_transmission",
    )
    # Price range queries ("show variants under ₹7,00,000")
    variant_collection.create_index(
        [("price_ex_showroom_inr", ASCENDING)],
        name="idx_variants_price",
    )

    print("OK: All indexes ensured.")


# Create indexes once on first import (idempotent — safe to run repeatedly)
ensure_indexes()