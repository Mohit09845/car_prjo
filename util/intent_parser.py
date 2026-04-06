from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from collections import OrderedDict
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# Ensure .env is loaded before reading env vars (required in Docker containers)
load_dotenv()

# LRU Cache for intent parsing to avoid redundant LLM operations
_INTENT_CACHE = OrderedDict()
MAX_CACHE_SIZE = 1000

# Use the ASYNC client to prevent blocking the FastAPI event loop
client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

class IntentResponse(BaseModel):
    intent: Literal[
        "get_all_cars",
        "get_car",
        "get_car_colors",
        "get_car_specs",
        "get_variants",
        "get_variant_detail",
        "get_car_complete_data",
        "compare_models",
        "compare_variants",
        "price_range",
        "unknown"
    ] = Field(description="The matching intent for the user's query.")

    model: Optional[str] = Field(None, description="The car model name if applicable.")
    models: Optional[List[str]] = Field(None, description="List of car models if comparing.")
    variant: Optional[str] = Field(None, description="The variant name if applicable.")
    variants: Optional[List[str]] = Field(None, description="List of variant names if comparing.")
    min_price: Optional[int] = Field(None, description="Minimum price in raw INR (5 lakh -> 500000).")
    max_price: Optional[int] = Field(None, description="Maximum price in raw INR (10 lakh -> 1000000).")

    fields: Optional[List[Literal[
        # ── Appearance ──────────────────────────────────────────────────────
        "colours",              # color, colour, shade, rang, color options

        # ── Engine & Performance ─────────────────────────────────────────────
        "engine",               # displacement, engine type, cc
        "power",                # bhp, horsepower, kitna power, power output
        "torque",               # nm, torque, pulling power
        "mileage",              # mileage, fuel efficiency, kmpl, average, kitna deti hai

        # ── Transmission ────────────────────────────────────────────────────
        "transmission",         # automatic, manual, AMT, CVT, AT, MT, gear type

        # ── Pricing ─────────────────────────────────────────────────────────
        "price_range_inr",      # ex-showroom price range of model
        "price_on_road",        # on-road price, total price, final price

        # ── Fuel ────────────────────────────────────────────────────────────
        "fuel_tank",            # fuel capacity, tank size, litres
        "fuel_type",            # petrol, diesel, CNG, hybrid, electric, EV

        # ── Dimensions & Space ──────────────────────────────────────────────
        "dimensions",           # size, length, width, height
        "boot_space",           # boot space, dicky, luggage space, trunk
        "ground_clearance",     # ground clearance, height from road, off-road
        "seating_capacity",     # seating, kitne log, seats, passengers, family size

        # ── Safety ──────────────────────────────────────────────────────────
        "safety",               # airbags, ABS, ESC, EBD, hill assist, ISOFIX
        "airbags",              # airbags specifically, kitne airbags
        "ncap",                 # NCAP rating, safety stars, crash test rating

        # ── Features & Tech ─────────────────────────────────────────────────
        "features",             # sunroof, infotainment, cruise control, wireless charger, ADAS
        "key_features",         # top features, highlights, standout features

        # ── Variants ────────────────────────────────────────────────────────
        "variants",             # available variants, trim levels

        # ── Reviews ─────────────────────────────────────────────────────────
        "reviews",              # rating, user feedback, kitne log pasand karte hain
    ]]] = Field(None, description="Specific fields the user is asking about. Only populate when user asks for a specific attribute.")


# Make this function ASYNC
async def extract_intent(query: str) -> dict:
    # ── Check Cache First ──
    if query in _INTENT_CACHE:
        _INTENT_CACHE.move_to_end(query)  # Mark as recently used
        print(f"⚡ Cache hit for query: '{query}'")
        return _INTENT_CACHE[query]

    system_prompt = """
You are a Maruti Suzuki car dealership API assistant intent parser.
Your job is to read user queries, normalize any phonetic mispronunciations of car models, and map the query strictly to the following JSON format.

{
  "intent": "get_all_cars" | "get_car" | "get_car_colors" | "get_car_specs" | "get_variants" | "get_variant_detail" | "get_car_complete_data" | "compare_models" | "compare_variants" | "price_range" | "unknown",
  "model": "Car model name if applicable (Normalized)",
  "models": ["List of normalized models if comparing"],
  "variant": "Variant name if applicable (e.g. ZXI, VXI)",
  "variants": ["List of variants if comparing"],
  "min_price": Minimum price in raw INR (e.g. 5 lakh -> 500000),
  "max_price": Maximum price in raw INR (e.g. 10 lakh -> 1000000),
  "fields": ["Specific fields user is asking about"]
}

---
CRITICAL STEP 1: SPELLING & PHONETIC NORMALIZATION
Because users speak via voice, STT transcripts often contain phonetic misspellings of Indian colloquial pronunciations. Before determining the intent or filling the JSON, you MUST map any of the following variations to their EXACT Official Name:
* WagonR: wagonar, wagonaaar, vagon r, bagonar, wagon r, wegnar
* Baleno: baleeno, balino, valeno, ballyno, beleno
* Brezza: breja, briza, bareeza, vrezza, brezzaa, vitara breja
* Dzire: desire, dezire, dijaire, dijire, dezir
* Swift: sift, suift, sifi, shwift, swipt
* Ertiga: artiga, aartiga, ertigga, irtega, aertiga
* Fronx: fronks, fornx, phronx, frongx, fronx
* Grand Vitara: grand bitara, girand vitara, vitara, garend vitara
* Jimny: jimni, chimni, zimny, gimny
* Celerio: selerio, salerio, celeriya, selario
* Alto K10: aalto, elto, alto kay ten, altok10
* Ignis: eegnis, ignees, iginis, aignis
* Eeco: ecko, ikko, iiko, eecko, eeco
* S-Presso: espreso, espresso, s preso, aspresso
* Ciaz: siyaz, shiaz, shiyaz, ciyaz, syaz
* XL6: exel six, x l 6, axel six, axel 6
* Invicto: inbicto, inviko, invikto
* Victoris: viktoris, biktoris, victoris, bictoris, victores, victorise
* e Vitara: e vitara, ev vitara, electric vitara, ivitara, e bitara
* Alto Tour H1: Alto Tuar H1, Alto Tuur H1, Alto Tour H1, Alto Ture H1, Alto Toor H1

Transmission term normalization:
* Automatic: automatik, aatamatic, ottometic, auto, aautomatic, automatic wali, auto wali
* AMT: amt, a m t, auto manual, automated manual
* CVT: cvt, c v t, continuously variable
* Manual: manuwal, manyual, MT, hand gear, haath wala gear

---
CRITICAL STEP 2: INTENT RULES
- "get_all_cars"          -> User wants ONLY a simple list of car model names. No attributes.
                             EXAMPLE: "show me all cars", "kaun kaun si cars hain"
- "get_car_complete_data" -> User asks about ANY attribute across ALL cars or ALL variants.
                             EXAMPLES: "all cars mileage", "saari cars ki mileage", "sabse zyada mileage wali car",
                             "most powerful variant", "cheapest variant overall", "all cars price list",
                             "automatic cars dikhao", "kaun si cars automatic hain", "which cars have AMT",
                             "kitni seating wali cars hain", "7 seater cars", "sabse zyada boot space"
                             STRICT RULE: If user asks about an attribute across the ENTIRE system -> ALWAYS use "get_car_complete_data".
                             HOWEVER: If they ask for "all cars of a SPECIFIC model" (e.g., "all manual cars of brezza", "brezza ki sabhi automatic cars"), USE "get_variants", NOT "get_car_complete_data".
- "get_car"               -> User wants full info about one specific model.
                             EXAMPLE: "tell me about Swift", "Baleno ki details do"
- "get_car_colors"        -> User asks specifically about colors of one model.
                             EXAMPLE: "Baleno ke colors kya hain", "what colors does Swift have"
                             Set fields: ["colours"]
- "get_car_specs"         -> User asks about specs of one model.
                             EXAMPLE: "Swift ki engine specs", "Baleno ka boot space", "Swift mein kitni seating hai",
                             "Brezza ka ground clearance", "Dzire ki on-road price", "Swift mein automatic hai kya"
                             Set fields accordingly.
- "get_variants"          -> User wants all variants of one specific model listed, or filtered variants of a specific model.
                             EXAMPLE: "Swift ke saare variants", "show variants of Baleno", "Brezza manual variants", "all automatic cars of Swift"
- "get_variant_detail"    -> User asks about one specific variant of a model.
                             EXAMPLE: "Swift VXI ki details", "Baleno Alpha ka price"
- "compare_models"        -> User wants to compare 2 or more car models.
                             EXAMPLE: "Swift vs Baleno", "compare Breja and Phronx"
- "compare_variants"      -> User wants to compare 2 or more variants of the same model.
                             EXAMPLE: "Swift LXI vs VXI vs ZXI"
- "price_range"           -> User filters cars/variants by budget.
                             EXAMPLE: "5 lakh se 8 lakh mein kaun si car", "cars under 10 lakh"
- "unknown"               -> Query is completely unrelated to cars.

Transmission-specific routing guide:
* "automatic cars" / "AMT wali cars"                      → get_car_complete_data, fields: ["transmission"]
* "Swift mein automatic hai kya" / "Baleno ka gear type"  → get_car_specs, model: <Model>, fields: ["transmission"]
* "automatic cars under 8 lakh"                           → price_range, fields: ["transmission"], max_price: <value>
* "Swift automatic vs manual"                             → compare_variants, fields: ["transmission"]

---
CRITICAL STEP 3: FIELDS RULES
Populate "fields" ONLY when user asks for a specific attribute, not full info.
Use EXACTLY these field names:

APPEARANCE:
- "colours"           -> color, colour, shade, rang, color options, kaunse rang

ENGINE & PERFORMANCE:
- "engine"            -> displacement, engine type, cc, engine specs
- "power"             -> bhp, horsepower, kitna power, power output, powerful
- "torque"            -> nm, torque, pulling power, torque output
- "mileage"           -> mileage, fuel efficiency, kmpl, average, kitna deti hai, fuel economy

TRANSMISSION:
- "transmission"      -> automatic, manual, AMT, CVT, AT, MT, gear type, auto gear,
                         automatic gearbox, auto wali, haath wala gear, self-drive

PRICING:
- "price_range_inr"   -> ex-showroom price, starting price, price of model
- "price_on_road"     -> on-road price, total price, final price, road pe kitna padega

FUEL:
- "fuel_tank"         -> fuel capacity, tank size, kitne litre ka tank
- "fuel_type"         -> petrol, diesel, CNG, hybrid, electric, EV, konsa fuel

DIMENSIONS & SPACE:
- "dimensions"        -> size, length, width, height, measurements
- "boot_space"        -> boot space, dicky, luggage space, trunk, kitna samaan
- "ground_clearance"  -> ground clearance, height from road, kitni uchi, off-road
- "seating_capacity"  -> seating, kitne log, seats, passengers, family size, 5 seater, 7 seater

SAFETY:
- "safety"            -> safety features, ABS, ESC, EBD, hill assist, ISOFIX, overall safety
- "airbags"           -> airbags, kitne airbags, airbag count
- "ncap"              -> NCAP rating, safety stars, crash test, star rating

FEATURES & TECH:
- "features"          -> sunroof, infotainment, cruise control, wireless charger, ADAS, tech features
- "key_features"      -> top features, highlights, kya kya milta hai, standout features

VARIANTS:
- "variants"          -> available variants, trim levels, kaun kaun se variants

REVIEWS:
- "reviews"           -> rating, user feedback, kitne log pasand karte hain, review, score

---
GENERAL RULES:
1. Normalize model names using the STT spelling list above. Always output the Official Name.
2. Convert lakh/thousand prices to raw INR integers (5 lakh -> 500000).
3. Return ONLY valid JSON. No markdown, no explanation, no extra text.
4. Omit keys that are not applicable (return null for them).
5. When user asks about seating → fields: ["seating_capacity"]
6. When user asks about boot space / dicky → fields: ["boot_space"]
7. When user asks about ground clearance → fields: ["ground_clearance"]
8. When user asks about on-road price → fields: ["price_on_road"]
9. When user asks about safety rating / NCAP stars → fields: ["ncap"]
10. When user asks about airbags count → fields: ["airbags"]
11. When user asks about power/bhp → fields: ["power"]
12. When user asks about torque → fields: ["torque"]
13. When user asks about fuel type (petrol/CNG/electric) → fields: ["fuel_type"]
"""

    try:
        response = await client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0,
            max_tokens=1024,
        )

        content = response.choices[0].message.content.strip()

        # Clean markdown code blocks if present
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        parsed_data = IntentResponse.model_validate_json(content)
        result = parsed_data.model_dump(exclude_none=True)
        
        # ── Save to Cache ──
        _INTENT_CACHE[query] = result
        if len(_INTENT_CACHE) > MAX_CACHE_SIZE:
            _INTENT_CACHE.popitem(last=False)  # Remove oldest entry
            
        return result

    except Exception as e:
        print(f"Intent parsing error: {e}")
        return {"intent": "unknown"}