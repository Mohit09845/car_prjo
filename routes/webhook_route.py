from fastapi import APIRouter, Request
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

    intent_data = extract_intent(query)
    print("🧠 Intent Data:", intent_data)

    intent = intent_data.get("intent")
    fields = intent_data.get("fields")

    # ── GET ALL CARS ──────────────────────────────────────────────────────────
    if intent == "get_all_cars":
        cars = get_all_cars()
        return {"action": "list_cars", "cars": cars}

    # ── GET CAR / COLORS / SPECS ──────────────────────────────────────────────
    elif intent in ("get_car", "get_car_colors", "get_car_specs"):
        model = intent_data.get("model")
        result = get_car_by_model(model)

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
        car = get_car_by_model(model)
        return {
            "action": "variants_list",
            "model": model,
            "variants": car["variants"] if car else []
        }

    # ── GET SINGLE VARIANT DETAIL ─────────────────────────────────────────────
    elif intent == "get_variant_detail":
        model = intent_data.get("model")
        variant = intent_data.get("variant")
        result = get_variant(model, variant)

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
            "result": compare_models(models)
        }

    # ── COMPARE VARIANTS ──────────────────────────────────────────────────────
    elif intent == "compare_variants":
        model = intent_data.get("model")
        variants = intent_data.get("variants", [])
        return {
            "action": "compare_variants",
            "model": model,
            "variants": variants,
            "result": compare_variants(model, variants)
        }

    # ── PRICE RANGE FILTER ────────────────────────────────────────────────────
    elif intent == "price_range":
        min_p = intent_data.get("min_price", 0)
        max_p = intent_data.get("max_price")
        return {
            "action": "price_range",
            "range": [min_p, max_p],
            "variants": get_variants_by_price_range(min_p, max_p)
        }
    
    elif intent == "get_car_complete_data":
        data = get_car_complete_data()
        return {
            "action": "car_complete_data",
            "count": len(data),
            "variants": data
        }

    # ── FALLBACK ──────────────────────────────────────────────────────────────
    return {"message": "Could not understand query"}