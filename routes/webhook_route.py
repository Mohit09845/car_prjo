from fastapi import APIRouter, Request
from fastapi.concurrency import run_in_threadpool
from controller.car_controller import (
    get_all_cars,
    get_car_by_model,
    get_variants_by_price_range,
    compare_models,
    compare_variants,
    get_variant,
    get_car_complete_data
)
from util.intent_parser import extract_intent
from util.field_filter import filter_response

router = APIRouter(prefix="/webhook", tags=["Webhook"])

@router.post("/elevenlabs")
async def elevenlabs_webhook(request: Request):
    print("\n🔥 ===== WEBHOOK CALLED =====")

    data = await request.json()
    query = (data.get("query") or data.get("text") or "").lower()

    print("🔎 Query:", query)

    # AWAIT the async intent parser so it doesn't block FastAPI
    intent_data = await extract_intent(query)
    print("🧠 Intent Data:", intent_data)

    intent = intent_data.get("intent")
    fields = intent_data.get("fields")

    # ── GET ALL CARS ──────────────────────────────────────────────────────────
    if intent == "get_all_cars":
        cars = await run_in_threadpool(get_all_cars)
        return {"action": "list_cars", "cars": cars}

    # ── GET CAR / COLORS / SPECS ──────────────────────────────────────────────
    elif intent in ("get_car", "get_car_colors", "get_car_specs"):
        model = intent_data.get("model")
        result = await run_in_threadpool(get_car_by_model, model)

        if fields and result:
            result = filter_response(result, fields)

        return {
            "action": "car_detail",
            "model": model,
            "data": result
        }

    # ── GET ALL VARIANTS OF A MODEL ───────────────────────────────────────────
    elif intent == "get_variants":
        model = intent_data.get("model")
        
        # If user explicitly asks for row-filtered variants, we need the detailed data
        if set(["transmission", "fuel_type", "colours", "seating_capacity"]) & set(fields or []):
            data = await run_in_threadpool(get_car_complete_data)
            # Filter to just this model
            data = [v for v in data if v.get("model", "").lower() == model.lower() if model]
            
            q_lower = query.lower()

            # Filter rows by transmission
            if "transmission" in (fields or []):
                if "manual" in q_lower or "mt" in q_lower or "manuwal" in q_lower:
                    data = [v for v in data if v.get("transmission", "").lower() == "manual"]
                elif "automatic" in q_lower or "amt" in q_lower or "cvt" in q_lower or "auto" in q_lower:
                    data = [v for v in data if v.get("transmission", "").lower() != "manual"]

            # Filter rows by fuel
            if "fuel_type" in (fields or []):
                if "cng" in q_lower:
                    data = [v for v in data if v.get("fuel", "").lower() == "cng"]
                elif "petrol" in q_lower:
                    data = [v for v in data if v.get("fuel", "").lower() == "petrol"]
                elif "diesel" in q_lower:
                    data = [v for v in data if v.get("fuel", "").lower() == "diesel"]
                elif "electric" in q_lower or "ev" in q_lower:
                    data = [v for v in data if v.get("fuel", "").lower() == "electric"]

            # Filter rows by color
            if "colours" in (fields or []):
                color_keywords = ["red", "white", "silver", "grey", "khaki", "brown", "black", "orange", "blue", "beige"]
                mentioned_colors = [c for c in color_keywords if c in q_lower]
                if mentioned_colors:
                    data = [
                        v for v in data 
                        if any(mc in [c_str.lower() for c_str in v.get("colours", [])] for mc in mentioned_colors)
                    ]

            return {
                "action": "variants_list_detailed",
                "model": model,
                "variants": data
            }

        # Otherwise just return the plain variant names
        car = await run_in_threadpool(get_car_by_model, model)
        return {
            "action": "variants_list",
            "model": model,
            "variants": car["variants"] if car else []
        }

    # ── GET SINGLE VARIANT DETAIL ─────────────────────────────────────────────
    elif intent == "get_variant_detail":
        model = intent_data.get("model")
        variant = intent_data.get("variant")
        result = await run_in_threadpool(get_variant, model, variant)

        if fields and result:
            result = filter_response(result, fields)

        return {
            "action": "variant_detail",
            "model": model,
            "variant": variant,
            "data": result
        }

    # ── COMPARE MODELS ────────────────────────────────────────────────────────
    elif intent == "compare_models":
        models = intent_data.get("models", [])
        return {
            "action": "compare_models",
            "models": models,
            "result": await run_in_threadpool(compare_models, models)
        }

    # ── COMPARE VARIANTS ──────────────────────────────────────────────────────
    elif intent == "compare_variants":
        model = intent_data.get("model")
        variants = intent_data.get("variants", [])
        return {
            "action": "compare_variants",
            "model": model,
            "variants": variants,
            "result": await run_in_threadpool(compare_variants, model, variants)
        }

    # ── PRICE RANGE FILTER ────────────────────────────────────────────────────
    elif intent == "price_range":
        min_p = intent_data.get("min_price", 0)
        max_p = intent_data.get("max_price")
        return {
            "action": "price_range",
            "range": [min_p, max_p],
            "variants": await run_in_threadpool(get_variants_by_price_range, min_p, max_p)
        }
    
    # ── COMPLETE CAR DATA ─────────────────────────────────────────────────────
    elif intent == "get_car_complete_data":
        data = await run_in_threadpool(get_car_complete_data)
        
        # FIX: If LLM mistakenly passed a model here, forcefully restrict the list to that model
        model = intent_data.get("model")
        if model:
            data = [v for v in data if v.get("model", "").lower() == model.lower()]

        # FIX: Dynamic row filtering across ALL cars
        if data:
            q_lower = query.lower()
            
            # 1. Transmission
            if "transmission" in (fields or []):
                if "manual" in q_lower or "mt" in q_lower or "manuwal" in q_lower:
                    data = [v for v in data if v.get("transmission", "").lower() == "manual"]
                elif "automatic" in q_lower or "amt" in q_lower or "cvt" in q_lower or "auto" in q_lower:
                    data = [v for v in data if v.get("transmission", "").lower() != "manual"]

            # 2. Fuel Type
            if "fuel_type" in (fields or []):
                if "cng" in q_lower:
                    data = [v for v in data if v.get("fuel", "").lower() == "cng"]
                elif "petrol" in q_lower:
                    data = [v for v in data if v.get("fuel", "").lower() == "petrol"]
                elif "electric" in q_lower or "ev" in q_lower:
                    data = [v for v in data if v.get("fuel", "").lower() == "electric"]

            # 3. Colors
            if "colours" in (fields or []):
                color_keywords = ["red", "white", "silver", "grey", "khaki", "brown", "black", "orange", "blue", "beige"]
                mentioned_colors = [c for c in color_keywords if c in q_lower]
                if mentioned_colors:
                    data = [
                        v for v in data 
                        if any(mc in [c_str.lower() for c_str in v.get("colours", [])] for mc in mentioned_colors)
                    ]

            # 4. Seating Capacity (e.g., "7 seater")
            if "seating_capacity" in (fields or []):
                if "7" in q_lower or "seven" in q_lower:
                    data = [v for v in data if v.get("seating_capacity") == 7]
                elif "5" in q_lower or "five" in q_lower:
                    data = [v for v in data if v.get("seating_capacity") == 5]
                elif "6" in q_lower or "six" in q_lower:
                    data = [v for v in data if v.get("seating_capacity") == 6]

        return {
            "action": "car_complete_data",
            "count": len(data) if data else 0,
            "variants": data
        }

    # ── FALLBACK ──────────────────────────────────────────────────────────────
    return {"message": "Could not understand query"}