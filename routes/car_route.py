from fastapi import APIRouter, HTTPException, Query
from controller.car_controller import (
    get_all_cars,
    get_car_by_model,
    get_variants_by_price_range,
    compare_models,
    compare_variants,
    get_variant,
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


# ── GET /cars/{model} ─────────────────────────────────────────────────────────
@router.get("/{model}")
def car_by_model(model: str):
    """
    Full car info for a model with human-readable colours.
    e.g. /cars/Swift
    """
    car = get_car_by_model(model)
    if not car:
        raise HTTPException(status_code=404, detail=f"Car model '{model}' not found.")
    return car


# ── GET /cars/price-range?min=500000&max=800000 ───────────────────────────────
@router.get("/filter/price-range")
def cars_by_price(
    min: int = Query(..., ge=0,          description="Min ex-showroom price in ₹"),
    max: int = Query(..., ge=0,          description="Max ex-showroom price in ₹"),
):
    """
    All variants whose ex-showroom price falls within [min, max].
    Sorted cheapest → most expensive.
    e.g. /cars/filter/price-range?min=500000&max=800000
    """
    if min > max:
        raise HTTPException(status_code=400, detail="'min' must be ≤ 'max'.")
    variants = get_variants_by_price_range(min, max)
    if not variants:
        raise HTTPException(status_code=404, detail="No variants found in this price range.")
    return {"count": len(variants), "variants": variants}


# ── POST /cars/compare/models ─────────────────────────────────────────────────
@router.post("/compare/models")
def compare_car_models(body: CompareModelsRequest):
    """
    Side-by-side comparison of two or more car models.
    Body: { "models": ["Swift", "Dzire"] }
    """
    if len(body.models) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 models to compare.")
    result = compare_models(body.models)
    if not result:
        raise HTTPException(status_code=404, detail="None of the requested models were found.")
    return {"compared": len(result), "cars": result}


# ── POST /cars/compare/variants ───────────────────────────────────────────────
@router.post("/compare/variants")
def compare_car_variants(body: CompareVariantsRequest):
    """
    Side-by-side comparison of specific variants within a car model.
    Body: { "car_model": "Swift", "variants": ["LXi", "VXi", "ZXi Plus AMT"] }
    """
    if len(body.variants) < 2:
        raise HTTPException(status_code=400, detail="Provide at least 2 variants to compare.")
    result = compare_variants(body.car_model, body.variants)
    if not result:
        raise HTTPException(status_code=404, detail="No matching variants found.")
    return {"car_model": body.car_model, "compared": len(result), "variants": result}


# ── GET /cars/{model}/variants/{variant_name} ─────────────────────────────────
@router.get("/{model}/variants/{variant_name}")
def variant_detail(model: str, variant_name: str):
    """
    Full spec for one specific variant.
    e.g. /cars/Swift/variants/ZXi Plus AMT
    """
    v = get_variant(model, variant_name)
    if not v:
        raise HTTPException(
            status_code=404,
            detail=f"Variant '{variant_name}' not found for model '{model}'.",
        )
    return v