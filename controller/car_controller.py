from database.connection import car_collection, variant_collection

# ═══════════════════════════════════════════════════════════════════════════════
#  COLOR  NORMALIZER
#  "Pearl Arctic White With Bluish Black Roof" → "White + Black"
#  "Sizzling Red"                              → "Red"
#  "Dual Tone Blue + Black"                    → "Blue + Black"
# ═══════════════════════════════════════════════════════════════════════════════

_COLOR_KEYWORDS = {
    # Whites
    "white":  "White",
    "arctic": "White",
    "pearl":  "White",

    # Reds
    "red":      "Red",
    "sizzling": "Red",
    "opulent":  "Red",
    "gallant":  "Red",

    # Blues
    "blue":     "Blue",
    "nexa":     "Blue",
    "poolside": "Blue",
    "luster":   "Blue",

    # Blacks
    "black": "Black",

    # Greys
    "grey":    "Grey",
    "gray":    "Grey",
    "magma":   "Grey",
    "grandeur":"Grey",

    # Silvers
    "silver": "Silver",
    "silky":  "Silver",
    "splendid":"Silver",

    # Browns
    "brown":   "Brown",
    "nutmeg":  "Brown",
    "bronze":  "Brown",
    "copper":  "Brown",

    # Oranges
    "orange": "Orange",
    "novel":  "Orange",

    # Greens
    "green":  "Green",
    "olive":  "Green",
    "khaki":  "Khaki",
    "brave":  "Khaki",

    # Beiges
    "beige": "Beige",
    "luxe":  "Beige",
    "cream": "Beige",

    # Yellows
    "yellow": "Yellow",
    "golden": "Yellow",
}


def _extract_color(text: str) -> str | None:
    """Return the first matching human color from a text fragment."""
    t = text.lower()
    for kw, label in _COLOR_KEYWORDS.items():
        if kw in t:
            return label
    return None


def _normalize_color(raw: str) -> str:
    """Convert any raw color string to a clean, human-readable label."""
    lower = raw.lower()

    is_dual = "with" in lower or "dual tone" in lower or "+" in lower

    if is_dual:
        # Split on "with" or "+"
        parts = lower.replace("dual tone", "").replace("+", " with ").split(" with ")
        colors = []
        for part in parts:
            c = _extract_color(part)
            if c and c not in colors:
                colors.append(c)
        return " + ".join(colors) if colors else raw

    return _extract_color(raw) or raw          # fallback to raw if no match


# ═══════════════════════════════════════════════════════════════════════════════
#  SHARED  HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _fmt_car(car: dict) -> dict:
    """Serialize a car document for API response."""
    car["_id"] = str(car["_id"])
    if "colours" in car:
        # normalize + deduplicate while preserving order
        seen, clean = set(), []
        for raw in car["colours"]:
            label = _normalize_color(raw)
            if label not in seen:
                seen.add(label)
                clean.append(label)
        car["colours"] = clean
    return car


def _fmt_variant(v: dict) -> dict:
    """Serialize a variant document for API response."""
    v["_id"]    = str(v["_id"])
    v["car_id"] = str(v["car_id"])
    return v


def _find_car(model: str):
    """Case-insensitive car lookup by model name."""
    return car_collection.find_one(
        {"model": {"$regex": f"^{model}$", "$options": "i"}}
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  0.  GET ALL CARS  (existing endpoint, cleaned up)
# ═══════════════════════════════════════════════════════════════════════════════

def get_all_cars() -> list[dict]:
    return [_fmt_car(car) for car in car_collection.find({}, {"_id": 1, "make": 1, "model": 1, "type": 1, "price_range_inr": 1})]


# ═══════════════════════════════════════════════════════════════════════════════
#  1.  GET CAR BY MODEL  — full info with normalized colours
# ═══════════════════════════════════════════════════════════════════════════════

def get_car_by_model(model: str) -> dict | None:
    car = _find_car(model)
    if not car:
        return None

    variant_names = variant_collection.find(
        {"car_id": car["_id"]},
        {"name": 1, "_id": 0}          
    ).sort("price_ex_showroom_inr", 1) 

    car = _fmt_car(car)
    car["variants"] = [v["name"] for v in variant_names]
    return car


# ═══════════════════════════════════════════════════════════════════════════════
#  2.  PRICE RANGE  — variants between min and max (ex-showroom, rupees)
# ═══════════════════════════════════════════════════════════════════════════════

def get_variants_by_price_range(min_price: int, max_price: int) -> list[dict]:
    """
    Returns all variants whose ex-showroom price falls within the given range.
    Results are sorted cheapest → most expensive.
    """
    cursor = variant_collection.find(
        {"price_ex_showroom_inr": {"$gte": min_price, "$lte": max_price}},
        {"car_id": 1, "name": 1, "fuel": 1, "transmission": 1,
         "price_ex_showroom_inr": 1, "price_on_road_inr": 1,
         "mileage": 1, "mileage_unit": 1},
    ).sort("price_ex_showroom_inr", 1)

    return [_fmt_variant(v) for v in cursor]


# ═══════════════════════════════════════════════════════════════════════════════
#  3a. COMPARE MODELS  — side-by-side car comparison
# ═══════════════════════════════════════════════════════════════════════════════

def compare_models(models: list[str]) -> list[dict]:
    """
    Side-by-side comparison of car models.
    Returns only fields that meaningfully differ and help a buyer decide.
    Strips: make (same brand), _id, abs/ebd/esc (all true), isofix,
            exact body dimensions, doors, seating (always 5).
    """
    result = []
 
    for model in models:
        car = _find_car(model)
        if not car:
            continue
 
        result.append({
            "model":            car["model"],
            "type":             car["type"],
            "price_range_inr":  car["price_range_inr"],
            "engine": {
                "displacement_cc": car["engine"]["displacement_cc"],
                "fuel_types":      car["engine"]["fuel_types"],
                "transmissions":   car["engine"]["transmissions"],
            },
            "boot_space_litres": car["dimensions"]["boot_space_litres"],
            "wheelbase_mm":      car["dimensions"]["wheelbase_mm"],
            "safety": {
                "airbags":    car["safety"]["airbags"],
                "ncap_stars": car["safety"]["ncap_stars"],
            },
            "colours":      _normalize_colours(car.get("colours", [])),
            "user_rating":  car["user_rating"],
            "review_count": car["review_count"],
        })
 
    return result
 
 
def _normalize_colours(colours: list[str]) -> list[str]:
    """Deduplicated, human-readable colour list."""
    seen, clean = set(), []
    for raw in colours:
        label = _normalize_color(raw)
        if label not in seen:
            seen.add(label)
            clean.append(label)
    return clean
 


# ═══════════════════════════════════════════════════════════════════════════════
#  3b. COMPARE VARIANTS  — side-by-side variant comparison within a model
# ═══════════════════════════════════════════════════════════════════════════════

def compare_variants(car_model: str, variant_names: list[str]) -> list[dict]:
    car = _find_car(car_model)
    if not car:
        return []

    result = []
    for name in variant_names:
        v = variant_collection.find_one({
            "car_id": car["_id"],
            "name": {"$regex": f"^{name}$", "$options": "i"},
        })
        if v:
            result.append({
                "name":                  v["name"],
                "fuel":                  v["fuel"],
                "transmission":          v["transmission"],
                "price_ex_showroom_inr": v["price_ex_showroom_inr"],
                "price_on_road_inr":     v["price_on_road_inr"],
                "mileage":               f"{v['mileage']} {v['mileage_unit']}",
                "key_features":          v["key_features"],
            })

    return result

# ═══════════════════════════════════════════════════════════════════════════════
#  4.  GET SPECIFIC VARIANT
# ═══════════════════════════════════════════════════════════════════════════════

def get_variant(car_model: str, variant_name: str) -> dict | None:
    """
    Returns complete info for one variant of a car.
    e.g. get_variant("Swift", "ZXi Plus AMT")
    """
    car = _find_car(car_model)
    if not car:
        return None

    v = variant_collection.find_one({
        "car_id": car["_id"],
        "name": {"$regex": f"^{variant_name}$", "$options": "i"},
    })
    return _fmt_variant(v) if v else None