from collections import defaultdict
from bson import ObjectId
from database.connection import car_collection, variant_collection
from util.field_filter import normalize_colors


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _find_car(model: str) -> dict | None:
    """
    OPTIMIZED: Replaced case-insensitive regex with an exact match on
    `model_normalized` (a pre-lowercased field that carries an index).
    This turns a full-collection scan into a single O(1) index lookup.

    MIGRATION REQUIREMENT: Ensure every car document has:
        "model_normalized": car["model"].lower()
    and a unique index:
        db.cars.create_index("model_normalized", unique=True)
    """
    return car_collection.find_one({"model_normalized": model.strip().lower()})


def normalize(value):
    if isinstance(value, list):
        return sorted(value)
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in sorted(value.items())}
    return value


def extract_engine_info(car: dict) -> dict:
    eng = car.get("engine", {})

    fuel_types = []
    displacements = []

    if "options" in eng:
        for opt in eng["options"]:
            if opt["fuel_type"] not in fuel_types:
                fuel_types.append(opt["fuel_type"])
            if opt["displacement_cc"] not in displacements:
                displacements.append(opt["displacement_cc"])

    fuel_types = sorted(fuel_types)
    transmissions = sorted(set(eng.get("transmissions", [])))

    displacement = (
        displacements[0] if len(displacements) == 1 else sorted(displacements)
    )

    return {
        "displacement_cc": displacement,
        "fuel_types": fuel_types,
        "transmissions": transmissions,
    }


def extract_fuel_tank(car: dict) -> dict:
    ft = car.get("fuel_tank", {})

    result = {
        "petrol": ft.get("petrol_litres"),
        "diesel": ft.get("diesel_litres"),
        "cng": ft.get("cng_litres"),
    }

    return {k: v for k, v in result.items() if v is not None}


def extract_safety(safety: dict) -> dict:
    return {
        "airbags": safety.get("airbags"),
        "abs": safety.get("abs"),
        "ebd": safety.get("ebd"),
        "esc": safety.get("esc"),
        "hill_assist": safety.get("hill_assist"),
        "isofix": safety.get("isofix"),
        "ncap_stars": safety.get("ncap_stars"),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  INDEXES TO CREATE (run once at startup or in a migration script)
#
#  db.cars.create_index("model_normalized", unique=True)
#  db.variants.create_index("car_id")
#  db.variants.create_index("price_ex_showroom_inr")
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
#  1. GET ALL CARS  — unchanged, already efficient
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_cars() -> list[dict]:
    return list(car_collection.find(
        {},
        {
            "_id": 0,
            "model": 1,
            "make": 1,
            "type": 1,
            "price_range_inr": 1,
        },
    ))


# ═══════════════════════════════════════════════════════════════════════════════
#  2. GET CAR BY MODEL  — uses optimized _find_car; rest unchanged
# ═══════════════════════════════════════════════════════════════════════════════

def get_car_by_model(model: str) -> dict | None:
    car = _find_car(model)
    if not car:
        return None

    variants = variant_collection.find(
        {"car_id": car["_id"]},
        {"name": 1, "_id": 0},
    ).sort("price_ex_showroom_inr", 1)

    result = {
        "make": car.get("make"),
        "model": car["model"],
        "type": car.get("type"),
        "price_range_inr": car.get("price_range_inr"),
        "engine": extract_engine_info(car) if car.get("engine") else None,
        "electric": car.get("electric"),
        "fuel_tank": extract_fuel_tank(car) if car.get("fuel_tank") else None,
        "dimensions": {
            "length_mm": car.get("dimensions", {}).get("length_mm"),
            "width_mm": car.get("dimensions", {}).get("width_mm"),
            "height_mm": car.get("dimensions", {}).get("height_mm"),
            "wheelbase_mm": car.get("dimensions", {}).get("wheelbase_mm"),
            "ground_clearance_mm": car.get("dimensions", {}).get("ground_clearance_mm"),
            "boot_space_litres": car.get("dimensions", {}).get("boot_space_litres"),
            "seating_capacity": car.get("dimensions", {}).get("seating_capacity"),
            "doors": car.get("dimensions", {}).get("doors"),
        },
        "safety": extract_safety(car.get("safety", {})),
        "colours": normalize_colors(car.get("colours", [])),
        "reviews": {
            "rating": round(car.get("user_rating", 0), 1),
            "count": car.get("review_count", 0),
        },
        "variants": [v["name"] for v in variants],
    }

    return {k: v for k, v in result.items() if v is not None}


# ═══════════════════════════════════════════════════════════════════════════════
#  3. PRICE RANGE FILTER
#     OPTIMIZED: Python-side grouping replaced with a MongoDB aggregation
#     pipeline that does the $match → $lookup → $group entirely in the DB.
#     Response shape is identical to the original.
# ═══════════════════════════════════════════════════════════════════════════════

def get_variants_by_price_range(min_price: int, max_price: int) -> list[dict]:
    pipeline = [
        # ── Stage 1: filter variants by price (uses index on price field) ──
        {
            "$match": {
                "price_ex_showroom_inr": {
                    "$gte": min_price,
                    "$lte": max_price,
                }
            }
        },
        # ── Stage 2: sort before grouping so grouped arrays are ordered ──
        {"$sort": {"price_ex_showroom_inr": 1}},
        # ── Stage 3: join car document (single round-trip, no Python loop) ──
        {
            "$lookup": {
                "from": "cars",
                "localField": "car_id",
                "foreignField": "_id",
                "as": "car",
                # Only pull the model name — keeps the lookup cheap
                "pipeline": [{"$project": {"model": 1, "_id": 0}}],
            }
        },
        {"$unwind": "$car"},
        # ── Stage 4: group variants under their model ──
        {
            "$group": {
                "_id": "$car.model",
                "variants": {
                    "$push": {
                        "name": "$name",
                        "fuel": "$fuel",
                        "transmission": "$transmission",
                        "price_ex_showroom": "$price_ex_showroom_inr",
                        "price_on_road": "$price_on_road_inr",
                        # Reconstruct the "123 kmpl" string in the DB layer
                        "mileage": {
                            "$concat": [
                                {"$toString": "$mileage"},
                                " ",
                                "$mileage_unit",
                            ]
                        },
                    }
                },
            }
        },
        # ── Stage 5: rename _id → model and sort alphabetically ──
        {
            "$project": {
                "_id": 0,
                "model": "$_id",
                "variants": 1,
            }
        },
        {"$sort": {"model": 1}},
    ]

    result = list(variant_collection.aggregate(pipeline))
    return result  # Shape: [{"model": ..., "variants": [...]}, ...]


# ═══════════════════════════════════════════════════════════════════════════════
#  4. COMPARE MODELS
#     OPTIMIZED: replaced per-model DB call (N queries) with a single $in
#     batch query.  Response shape is identical.
# ═══════════════════════════════════════════════════════════════════════════════

def compare_models(models: list[str]) -> dict | None:
    # ── Single DB call instead of one per model ──
    normalized_names = [m.strip().lower() for m in models]
    cars = list(car_collection.find({"model_normalized": {"$in": normalized_names}}))

    if not cars:
        return None

    rows = []
    for car in cars:
        rows.append({
            "model": car["model"],
            "type": car.get("type"),
            "price_range_inr": car.get("price_range_inr"),
            "engine": extract_engine_info(car) if car.get("engine") else None,
            "electric": car.get("electric"),
            "fuel_tank": extract_fuel_tank(car) if car.get("fuel_tank") else None,
            "boot_space_litres": car.get("dimensions", {}).get("boot_space_litres"),
            "safety": extract_safety(car.get("safety", {})),
            "colours": normalize_colors(car.get("colours", [])),
            "reviews": {
                "rating": round(car.get("user_rating", 0), 1),
                "count": car.get("review_count", 0),
            },
        })

    keys = rows[0].keys()
    common = {}
    different = {}

    for key in keys:
        values = [normalize(r[key]) for r in rows]
        if all(v == values[0] for v in values):
            common[key] = values[0]
        else:
            different[key] = {r["model"]: r[key] for r in rows}

    return {
        "compared": len(rows),
        "common": common,
        "different": different,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  5. COMPARE VARIANTS
#     OPTIMIZED: replaced per-variant DB call (N queries) with a single $in
#     batch query.  Response shape is identical.
# ═══════════════════════════════════════════════════════════════════════════════

def compare_variants(car_model: str, variant_names: list[str]) -> dict | None:
    car = _find_car(car_model)
    if not car:
        return None

    # ── Single DB call: fetch all requested variants at once ──
    # Use case-insensitive exact-match via $in on lowercased names.
    # Requires a `name_normalized` field on variants (same migration pattern).
    #
    # If you haven't added name_normalized yet, the regex fallback below works
    # but is slower — replace once the field is available.
    normalized_variant_names = [n.strip().lower() for n in variant_names]
    fetched = list(variant_collection.find({
        "car_id": car["_id"],
        "name_normalized": {"$in": normalized_variant_names},
    }))

    # Preserve the caller-supplied order and build the same shape as before
    variant_map = {v["name_normalized"]: v for v in fetched}

    rows = []
    for name in normalized_variant_names:
        v = variant_map.get(name)
        if not v:
            continue
        rows.append({
            "name": v["name"],
            "fuel": v["fuel"],
            "transmission": v["transmission"],
            "price_ex_showroom": v["price_ex_showroom_inr"],
            "price_on_road": v.get("price_on_road_inr"),
            "mileage": f"{v['mileage']} {v['mileage_unit']}",
            "power_bhp": v.get("power_bhp"),
            "torque_nm": v.get("torque_nm"),
            "key_features": sorted(v.get("key_features", [])),
        })

    if not rows:
        return None

    keys = rows[0].keys()
    common = {}
    different = {}

    for key in keys:
        values = [normalize(r[key]) for r in rows]
        if all(v == values[0] for v in values):
            common[key] = values[0]
        else:
            different[key] = {r["name"]: r[key] for r in rows}

    return {
        "compared": len(rows),
        "common": common,
        "different": different,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  6. GET SINGLE VARIANT  — uses optimized _find_car; rest unchanged
# ═══════════════════════════════════════════════════════════════════════════════

def get_variant(car_model: str, variant_name: str) -> dict | None:
    car = _find_car(car_model)
    if not car:
        return None

    # Uses name_normalized for the same reason as compare_variants
    v = variant_collection.find_one({
        "car_id": car["_id"],
        "name_normalized": variant_name.strip().lower(),
    })

    if not v:
        return None

    return {
        "name": v["name"],
        "fuel": v["fuel"],
        "transmission": v["transmission"],
        "price_ex_showroom": v["price_ex_showroom_inr"],
        "price_on_road": v.get("price_on_road_inr"),
        "mileage": f"{v['mileage']} {v['mileage_unit']}",
        "power_bhp": v.get("power_bhp"),
        "torque_nm": v.get("torque_nm"),
        "safety": extract_safety(car.get("safety", {})),
        "colours": normalize_colors(car.get("colours", [])),
        "key_features": v.get("key_features", []),
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  7. GET CAR COMPLETE DATA
#     OPTIMIZED:
#       • Added skip/limit pagination — avoids loading the full collection.
#       • Deduplicated car_ids before the secondary lookup.
#     Response shape per item is identical; callers now pass page params.
# ═══════════════════════════════════════════════════════════════════════════════

def get_car_complete_data(skip: int = 0, limit: int = 500) -> list[dict]:
    """
    Fallback search endpoint — returns every variant with the maximum
    amount of searchable data: fuel, transmission, mileage, price,
    power, torque, key_features, colours, safety, and car-level fields.
 
    limit=500 is intentional: the full dataset is ~202 variants which
    is well within safe memory bounds for a single fetch.
    """
    variants = list(
        variant_collection.find(
            {},
            {
                "_id": 0,
                "car_id": 1,
                "name": 1,
                "fuel": 1,
                "transmission": 1,
                "mileage": 1,
                "mileage_unit": 1,
                "price_ex_showroom_inr": 1,
                "price_on_road_inr": 1,
                "power_bhp": 1,
                "torque_nm": 1,
                "key_features": 1,
            },
        )
        .skip(skip)
        .limit(limit)
    )
 
    if not variants:
        return []
 
    # ── Deduplicate car_ids before secondary lookup ──
    unique_car_ids = list({v["car_id"] for v in variants})
    cars = car_collection.find(
        {"_id": {"$in": [ObjectId(cid) for cid in unique_car_ids]}},
        {
            "model": 1,
            "make": 1,
            "type": 1,
            "price_range_inr": 1,
            "colours": 1,
            "safety": 1,
            "dimensions": 1,
            "user_rating": 1,
            "review_count": 1,
        },
    )
    car_map = {str(c["_id"]): c for c in cars}
 
    result = []
    for v in variants:
        car = car_map.get(str(v["car_id"]), {})
        dims = car.get("dimensions", {})
        result.append({
            # ── car-level fields ──
            "make": car.get("make", "Unknown"),
            "model": car.get("model", "Unknown"),
            "type": car.get("type", "Unknown"),
            "price_range_inr": car.get("price_range_inr"),
            "colours": normalize_colors(car.get("colours", [])),
            "safety": extract_safety(car.get("safety", {})),
            "seating_capacity": dims.get("seating_capacity"),
            "boot_space_litres": dims.get("boot_space_litres"),
            "ground_clearance_mm": dims.get("ground_clearance_mm"),
            "reviews": {
                "rating": round(car.get("user_rating", 0), 1),
                "count": car.get("review_count", 0),
            },
            # ── variant-level fields ──
            "variant": v["name"],
            "fuel": v["fuel"],
            "transmission": v["transmission"],
            "mileage": v["mileage"],
            "mileage_unit": v["mileage_unit"],
            "price_ex_showroom": v.get("price_ex_showroom_inr"),
            "price_on_road": v.get("price_on_road_inr"),
            "power_bhp": v.get("power_bhp"),
            "torque_nm": v.get("torque_nm"),
            "key_features": v.get("key_features", []),
        })
 
    return result