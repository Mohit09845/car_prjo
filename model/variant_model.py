from pydantic import BaseModel
from typing import List, Literal, Optional


class Variant(BaseModel):
    car_id: str
    name: str
    variant_code: Optional[str] = None

    fuel: Literal["Petrol", "CNG", "Diesel", "Hybrid"]
    transmission: Literal["Manual", "AMT", "Automatic", "CVT"]

    price_ex_showroom_inr: int
    price_on_road_inr: int

    mileage: float
    mileage_unit: Literal["kmpl", "km/kg"]

    power_bhp: float
    torque_nm: float

    key_features: List[str]