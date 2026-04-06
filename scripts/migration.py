"""
migration.py — run ONCE before deploying the optimized controller.

Place this file inside scripts/ (same folder as seed_data.py).
Run from the project root:
    python scripts/migration.py
"""

from pymongo.errors import OperationFailure
from database.connection import get_db


def safe_create_index(col, keys, label, **kwargs):
    """
    Create an index, but skip gracefully if one already exists on
    the same field(s) under a different name (OperationFailure code 85).
    """
    try:
        col.create_index(keys, **kwargs)
        print(f"   ✅ {label}")
    except OperationFailure as e:
        if e.code == 85:    # IndexOptionsConflict — same keys, different name
            print(f"   ⚠️  {label}  → already exists under a different name, skipped")
        elif e.code == 86:  # IndexKeySpecsConflict
            print(f"   ⚠️  {label}  → key spec conflict, skipped")
        else:
            raise           # re-raise anything unexpected


def migrate():
    db = get_db()
    cars_col = db["cars"]
    variants_col = db["variants"]

    # ── Step 1: backfill model_normalized on cars ──────────────────────────
    print("── Step 1: backfilling model_normalized on cars ──")
    cars = list(cars_col.find({}, {"_id": 1, "model": 1}))
    for car in cars:
        cars_col.update_one(
            {"_id": car["_id"]},
            {"$set": {"model_normalized": car["model"].strip().lower()}},
        )
    print(f"   Updated {len(cars)} car documents.\n")

    # ── Step 2: backfill name_normalized on variants ───────────────────────
    print("── Step 2: backfilling name_normalized on variants ──")
    variants = list(variants_col.find({}, {"_id": 1, "name": 1}))
    for v in variants:
        variants_col.update_one(
            {"_id": v["_id"]},
            {"$set": {"name_normalized": v["name"].strip().lower()}},
        )
    print(f"   Updated {len(variants)} variant documents.\n")

    # ── Step 3: ensure indexes (safe — skips if already exists) ───────────
    print("── Step 3: ensuring indexes ──")

    safe_create_index(
        cars_col, "model_normalized",
        "cars.model_normalized  (unique)",
        unique=True, name="idx_model_normalized"
    )
    safe_create_index(
        variants_col, "car_id",
        "variants.car_id",
        name="idx_variant_car_id"
    )
    safe_create_index(
        variants_col, "price_ex_showroom_inr",
        "variants.price_ex_showroom_inr",
        name="idx_variant_price"
    )
    safe_create_index(
        variants_col, [("car_id", 1), ("name_normalized", 1)],
        "variants.(car_id + name_normalized)  compound unique",
        unique=True, name="idx_variant_car_name"
    )

    print("\n✅ Migration complete. You can now deploy the optimized controller.")


if __name__ == "__main__":
    migrate()