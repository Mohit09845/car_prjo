from fastapi import APIRouter, HTTPException, Query

from controller.car_controller import (
    get_all_cars,
    get_car_by_model,
    get_variants_by_price_range,
    compare_models,
    compare_variants,
    get_variant,
    get_car_complete_data
)
from model.request_model import CompareModelsRequest, CompareVariantsRequest

router = APIRouter(prefix="/cars", tags=["Cars"])


# ── GET /cars ─────────────────────────────────────────────────────────────────
@router.get("/")
def list_cars():
    """Returns a lightweight list of all available car models."""
    cars = get_all_cars()
    if not cars:
        raise HTTPException(status_code=404, detail="No cars found.")
    return {"count": len(cars), "cars": cars}


# ── GET /cars/variants/all ────────────────────────────────────────────────────
# ✅ MOVED UP — must be before /{model} to avoid "variants" being treated as model name
@router.get("/variants/all")
def car_complete_data():
    """Returns all variants across all models with mileage and specs."""
    data = get_car_complete_data()
    if not data:
        raise HTTPException(status_code=404, detail="No variants found.")
    return {"count": len(data), "variants": data}


# ── GET /cars/filter/price-range ──────────────────────────────────────────────
@router.get("/filter/price-range")
def cars_by_price(
    min: int = Query(..., ge=0, description="Min ex-showroom price in ₹"),
    max: int = Query(..., ge=0, description="Max ex-showroom price in ₹"),
):
    if min > max:
        raise HTTPException(status_code=400, detail="'min' must be ≤ 'max'.")
    variants = get_variants_by_price_range(min, max)
    if not variants:
        raise HTTPException(status_code=404, detail="No variants found in this price range.")
    return {"count": len(variants), "variants": variants}


# ── POST /cars/compare/models ─────────────────────────────────────────────────
@router.post("/compare/models")
def compare_car_models(body: CompareModelsRequest):
    if len(body.models) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 models to compare.")
    result = compare_models(body.models)
    if not result:
        raise HTTPException(status_code=404, detail="None of the requested models were found.")
    if result["compared"] < 2:
        raise HTTPException(
            status_code=404,
            detail="Fewer than 2 models exist in the database for this comparison.",
        )
    return result


# ── POST /cars/compare/variants ───────────────────────────────────────────────
@router.post("/compare/variants")
def compare_car_variants(body: CompareVariantsRequest):
    if len(body.variants) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 variants to compare.")
    result = compare_variants(body.car_model, body.variants)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Car model not found or no matching variants.",
        )
    if result["compared"] < 2:
        raise HTTPException(
            status_code=404,
            detail="Fewer than 2 variants were found for this comparison.",
        )
    return {"car_model": body.car_model, **result}


# ── GET /cars/{model}/variants/{variant_name} ─────────────────────────────────
@router.get("/{model}/variants/{variant_name}")
def variant_detail(model: str, variant_name: str):
    v = get_variant(model, variant_name)
    if not v:
        raise HTTPException(
            status_code=404,
            detail=f"Variant '{variant_name}' not found for model '{model}'.",
        )
    return v


# ── GET /cars/{model} ─────────────────────────────────────────────────────────
# ✅ MUST always be last — catches any /{model} pattern
@router.get("/{model}")
def car_by_model(model: str):
    car = get_car_by_model(model)
    if not car:
        raise HTTPException(status_code=404, detail=f"Car model '{model}' not found.")
    return car