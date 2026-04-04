from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from openai import OpenAI
import os

client = OpenAI(
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
    min_price: Optional[int] = Field(None, description="Minimum price in raw INR (5 lakh → 500000).")
    max_price: Optional[int] = Field(None, description="Maximum price in raw INR (10 lakh → 1000000).")

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


def extract_intent(query: str) -> dict:
    system_prompt = """
You are a Maruti Suzuki car dealership API assistant intent parser.
Your job is to read user queries and map them strictly to the following JSON format.

{
  "intent": "get_all_cars" | "get_car" | "get_car_colors" | "get_car_specs" | "get_variants" | "get_variant_detail" | "get_car_complete_data" | "compare_models" | "compare_variants" | "price_range" | "unknown",
  "model": "Car model name if applicable",
  "models": ["List of models if comparing"],
  "variant": "Variant name if applicable (e.g. ZXI, VXI)",
  "variants": ["List of variants if comparing"],
  "min_price": Minimum price in raw INR (e.g. 5 lakh → 500000),
  "max_price": Maximum price in raw INR (e.g. 10 lakh → 1000000),
  "fields": ["Specific fields user is asking about e.g. colours, engine, mileage, safety"]
}

INTENT RULES:
- "get_all_cars"          → User wants ONLY a simple list of car model names. No attributes.
                            EXAMPLE: "show me all cars", "kaun kaun si cars hain"

- "get_car_complete_data" → User asks about ANY attribute (mileage, price, power, specs)
                            across ALL cars or ALL variants.
                            EXAMPLES:
                            "all cars mileage"
                            "saari cars ki mileage"
                            "mujhe sari cars ke milege chaiye"
                            "avg mileage of all cars"
                            "sabse zyada mileage wali car"
                            "most powerful variant"
                            "cheapest variant overall"
                            "all cars price list"
                            "sabhi cars ki power kitni hai"
                            STRICT RULE: If user asks about ANY attribute of ALL cars
                            → ALWAYS use "get_car_complete_data", NEVER "get_all_cars".

- "get_car"               → User wants full info about one specific model.
                            EXAMPLE: "tell me about Swift", "Baleno ki details do"

- "get_car_colors"        → User asks specifically about colors of one model.
                            EXAMPLE: "Baleno ke colors kya hain", "what colors does Swift have"
                            Set fields: ["colours"]

- "get_car_specs"         → User asks about specs of one model.
                            EXAMPLE: "Swift ki engine specs", "Baleno ka boot space"
                            Set fields accordingly.

- "get_variants"          → User wants all variants of one specific model listed.
                            EXAMPLE: "Swift ke saare variants", "show variants of Baleno"

- "get_variant_detail"    → User asks about one specific variant of a model.
                            EXAMPLE: "Swift VXI ki details", "Baleno Alpha ka price"

- "compare_models"        → User wants to compare 2 or more car models.
                            EXAMPLE: "Swift vs Baleno", "compare Brezza and Fronx"

- "compare_variants"      → User wants to compare 2 or more variants of the same model.
                            EXAMPLE: "Swift LXI vs VXI vs ZXI"

- "price_range"           → User filters cars/variants by budget.
                            EXAMPLE: "5 lakh se 8 lakh mein kaun si car", "cars under 10 lakh"

- "unknown"               → Query is completely unrelated to cars.

FIELDS RULES:
- Populate "fields" ONLY when user asks for a specific attribute, not full info.
- "colours"         → color, colour, shade, rang
- "engine"          → displacement, power, torque, engine type
- "dimensions"      → size, length, width, height, boot space, ground clearance
- "safety"          → airbags, NCAP, ABS, ESP
- "fuel_tank"       → fuel capacity, tank size
- "reviews"         → rating, reviews, user feedback
- "mileage"         → mileage, fuel efficiency, kmpl, kitna deti hai
- "features"        → sunroof, infotainment, cruise control, wireless charger
- "price_range_inr" → price of the model overall

GENERAL RULES:
- Normalize model names (e.g. "brezza" → "Brezza", "swift" → "Swift", "baleno" → "Baleno").
- Convert lakh/thousand prices to raw INR integers (5 lakh → 500000).
- Return ONLY valid JSON. No markdown, no explanation, no extra text.
- Omit keys that are not applicable (return null for them).
"""

    try:
        response = client.chat.completions.create(
            model="meta/llama-3.1-405b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0,
            max_tokens=1024,
        )

        content = response.choices[0].message.content.strip()

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