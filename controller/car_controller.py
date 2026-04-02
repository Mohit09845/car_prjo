import re
from collections import defaultdict
from bson import ObjectId
from database.connection import car_collection, variant_collection


# ═══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _find_car(model: str):
    return car_collection.find_one(
        {"model": {"$regex": f"^{re.escape(model)}$", "$options": "i"}}
    )


def normalize(value):
    if isinstance(value, list):
        return sorted(value)
    if isinstance(value, dict):
        return {k: normalize(v) for k, v in sorted(value.items())}
    return value


def extract_engine_info(car: dict):
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
        "transmissions": transmissions
    }


def extract_fuel_tank(car: dict):
    ft = car.get("fuel_tank", {})

    result = {
        "petrol": ft.get("petrol_litres"),
        "diesel": ft.get("diesel_litres"),
        "cng": ft.get("cng_kg"),
    }

    return {k: v for k, v in result.items() if v is not None}


# ═══════════════════════════════════════════════════════════════════════════════
#  1. GET ALL CARS
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_cars() -> list[dict]:
    return list(car_collection.find(
        {},
        {
            "_id": 0,
            "model": 1,
            "type": 1,
            "price_range_inr": 1
        }
    ))


# ═══════════════════════════════════════════════════════════════════════════════
#  2. GET CAR BY MODEL
# ═══════════════════════════════════════════════════════════════════════════════

def get_car_by_model(model: str) -> dict | None:
    car = _find_car(model)
    if not car:
        return None

    variants = variant_collection.find(
        {"car_id": car["_id"]},
        {"name": 1, "_id": 0}
    ).sort("price_ex_showroom_inr", 1)

    return {
        "model": car["model"],
        "type": car["type"],
        "price_range_inr": car["price_range_inr"],
        "engine": extract_engine_info(car),          # ✅ FIXED
        "fuel_tank": extract_fuel_tank(car),         # ✅ FIXED
        "variants": [v["name"] for v in variants]
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  3. PRICE RANGE FILTER
# ═══════════════════════════════════════════════════════════════════════════════

def get_variants_by_price_range(min_price: int, max_price: int) -> list[dict]:
    cursor = variant_collection.find(
        {
            "price_ex_showroom_inr": {
                "$gte": min_price,
                "$lte": max_price
            }
        },
        {
            "car_id": 1,
            "name": 1,
            "fuel": 1,
            "transmission": 1,
            "price_ex_showroom_inr": 1,
            "mileage": 1,
            "mileage_unit": 1,
        },
    ).sort("price_ex_showroom_inr", 1)

    variants = list(cursor)
    if not variants:
        return []

    grouped = defaultdict(list)
    for v in variants:
        grouped[str(v["car_id"])].append(v)

    car_ids = [ObjectId(cid) for cid in grouped.keys()]
    cars = car_collection.find({"_id": {"$in": car_ids}}, {"model": 1})

    car_map = {str(c["_id"]): c["model"] for c in cars}

    result = []
    for car_id, vars in grouped.items():
        result.append({
            "model": car_map.get(car_id, "Unknown"),
            "variants": [
                {
                    "name": v["name"],
                    "fuel": v["fuel"],
                    "transmission": v["transmission"],
                    "price": v["price_ex_showroom_inr"],
                    "mileage": f"{v['mileage']} {v['mileage_unit']}"
                }
                for v in vars
            ]
        })

    result.sort(key=lambda x: x["model"])
    return result


# ═══════════════════════════════════════════════════════════════════════════════
#  4. COMPARE MODELS
# ═══════════════════════════════════════════════════════════════════════════════

def compare_models(models: list[str]) -> dict | None:
    rows = []

    for model in models:
        car = _find_car(model)
        if not car:
            continue

        rows.append({
            "model": car["model"],
            "type": car["type"],
            "price_range_inr": car["price_range_inr"],
            "engine": extract_engine_info(car),      # ✅ FIXED
            "fuel_tank": extract_fuel_tank(car),     # ✅ FIXED
            "boot_space_litres": car["dimensions"]["boot_space_litres"],
            "safety": {
                "airbags": car["safety"]["airbags"],
                "ncap": car["safety"]["ncap_stars"],
            },
            "reviews": {
                "rating": round(car.get("user_rating", 0), 1),
                "count": car.get("review_count", 0)
            }
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
            different[key] = {r["model"]: r[key] for r in rows}

    return {
        "compared": len(rows),
        "common": common,
        "different": different
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  5. COMPARE VARIANTS
# ═══════════════════════════════════════════════════════════════════════════════

def compare_variants(car_model: str, variant_names: list[str]) -> dict | None:
    car = _find_car(car_model)
    if not car:
        return None

    rows = []
    for name in variant_names:
        v = variant_collection.find_one({
            "car_id": car["_id"],
            "name": {"$regex": f"^{re.escape(name)}$", "$options": "i"},
        })

        if v:
            rows.append({
                "name": v["name"],
                "fuel": v["fuel"],
                "transmission": v["transmission"],
                "price": v["price_ex_showroom_inr"],
                "mileage": f"{v['mileage']} {v['mileage_unit']}",
                "key_features": sorted(v.get("key_features", []))
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
        "different": different
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  6. GET SINGLE VARIANT
# ═══════════════════════════════════════════════════════════════════════════════

def get_variant(car_model: str, variant_name: str) -> dict | None:
    car = _find_car(car_model)
    if not car:
        return None

    v = variant_collection.find_one({
        "car_id": car["_id"],
        "name": {"$regex": f"^{re.escape(variant_name)}$", "$options": "i"},
    })

    if not v:
        return None

    return {
        "name": v["name"],
        "fuel": v["fuel"],
        "transmission": v["transmission"],
        "price": v["price_ex_showroom_inr"],
        "mileage": f"{v['mileage']} {v['mileage_unit']}",
        "key_features": v.get("key_features", [])
    }