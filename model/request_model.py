from pydantic import BaseModel


# ── Request bodies for POST endpoints ────────────────────────────────────────
#    These are NOT MongoDB blueprints — they only validate incoming API payloads

class CompareModelsRequest(BaseModel):
    models: list[str]           # ["Swift", "Dzire"]


class CompareVariantsRequest(BaseModel):
    car_model: str              # "Swift"
    variants: list[str]         # ["LXi", "VXi", "ZXi Plus AMT"]