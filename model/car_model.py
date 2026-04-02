from pydantic import BaseModel
from typing import List, Optional, Literal


class PriceRange(BaseModel):
    min_ex_showroom: int
    max_ex_showroom: int


class EngineOption(BaseModel):
    displacement_cc: int
    cylinders: int
    fuel_type: str


class Engine(BaseModel):
    options: List[EngineOption]
    transmissions: List[str]


class FuelTank(BaseModel):
    petrol_litres: Optional[int] = None
    diesel_litres: Optional[int] = None
    cng_kg: Optional[float] = None


class Dimensions(BaseModel):
    length_mm: int
    width_mm: int
    height_mm: int
    wheelbase_mm: int
    ground_clearance_mm: int
    boot_space_litres: int
    seating_capacity: int
    doors: int


class Safety(BaseModel):
    airbags: int
    abs: bool
    ebd: bool
    esc: bool
    hill_assist: bool
    isofix: bool
    ncap_stars: Optional[int] = None


class Car(BaseModel):
    make: str
    model: str
    type: str
    price_range_inr: PriceRange
    engine: Engine
    fuel_tank: FuelTank
    dimensions: Dimensions
    safety: Safety
    colours: List[str]
    user_rating: float
    review_count: int


class Variant(BaseModel):
    car_id: str
    name: str
    fuel: Literal["Petrol", "CNG", "Diesel", "Hybrid"]
    transmission: Literal["Manual", "AMT", "Automatic", "CVT"]
    price_ex_showroom_inr: int
    price_on_road_inr: int
    mileage: float
    mileage_unit: str
    power_bhp: float
    torque_nm: float
    key_features: List[str]