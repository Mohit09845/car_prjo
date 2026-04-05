from pydantic import BaseModel
from typing import List, Literal, Optional

Fuel = Literal["Petrol", "CNG", "Diesel", "Hybrid", "Electric"]
Transmission = Literal["Manual", "Automatic", "CVT"]
MileageUnit = Literal["kmpl", "km/kg", "km/charge"]


class Variant(BaseModel):
    car_id: str
    name: str
    variant_code: Optional[str] = None

    fuel: Fuel
    transmission: Transmission

    price_ex_showroom_inr: int
    price_on_road_inr: int

    mileage: float
    mileage_unit: MileageUnit

    power_bhp: float
    torque_nm: float

    key_features: List[str]


class VariantSeed(BaseModel):
    """Variant row in seed data before resolving car_id."""

    car_model: str
    name: str
    variant_code: Optional[str] = None

    fuel: Fuel
    transmission: Transmission

    price_ex_showroom_inr: int
    price_on_road_inr: int

    mileage: float
    mileage_unit: MileageUnit

    power_bhp: float
    torque_nm: float

    key_features: List[str]
