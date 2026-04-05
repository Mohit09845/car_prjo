from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from openai import AsyncOpenAI
import os

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
        "colours",
        "engine",
        "dimensions",
        "safety",
        "fuel_tank",
        "reviews",
        "price_range_inr",
        "variants",
        "features",
        "mileage"
    ]]] = Field(None, description="Specific fields the user is asking about. Only populate when user asks for a specific attribute.")

# Make this function ASYNC
async def extract_intent(query: str) -> dict:
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
  "fields": ["Specific fields user is asking about e.g. colors, engine, mileage, safety"]
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

---
CRITICAL STEP 2: INTENT RULES
- "get_all_cars"          -> User wants ONLY a simple list of car model names.
- "get_car_complete_data" -> User asks about ANY attribute (mileage, price, power, specs) across ALL cars or ALL variants. (e.g., "all cars mileage", "sabse zyada mileage wali car"). STRICT RULE: If user asks about ANY attribute of ALL cars -> ALWAYS use "get_car_complete_data".
- "get_car"               -> User wants full info about one specific model.
- "get_car_colors"        -> User asks specifically about colors of one model. Set fields: ["colours"]
- "get_car_specs"         -> User asks about specs of one model.
- "get_variants"          -> User wants all variants of one specific model listed.
- "get_variant_detail"    -> User asks about one specific variant of a model.
- "compare_models"        -> User wants to compare 2 or more car models.
- "compare_variants"      -> User wants to compare 2 or more variants of the same model.
- "price_range"           -> User filters cars/variants by budget.
- "unknown"               -> Query is completely unrelated to cars.

---
CRITICAL STEP 3: FIELDS RULES
Populate "fields" ONLY when user asks for a specific attribute, not full info.
- "colours"         -> color, colour, shade, rang
- "engine"          -> displacement, power, torque, engine type
- "dimensions"      -> size, length, width, height, boot space, ground clearance
- "safety"          -> airbags, NCAP, ABS, ESP
- "fuel_tank"       -> fuel capacity, tank size
- "reviews"         -> rating, reviews, user feedback
- "mileage"         -> mileage, fuel efficiency, kmpl, kitna deti hai
- "features"        -> sunroof, infotainment, cruise control, wireless charger
- "price_range_inr" -> price of the model overall

---
GENERAL RULES:
1. Normalize model names using the STT spelling list provided above. Always output the Official Name.
2. Convert lakh/thousand prices to raw INR integers (5 lakh -> 500000).
3. Return ONLY valid JSON. No markdown, no explanation, no extra text.
4. Omit keys that are not applicable (return null for them).
"""

    try:
        # Await the response
        response = await client.chat.completions.create(
            model="meta/llama-3.1-70b-instruct", # 70B is much faster for JSON than 405B
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
        return parsed_data.model_dump(exclude_none=True)

    except Exception as e:
        print(f"Intent parsing error: {e}")
        return {"intent": "unknown"}