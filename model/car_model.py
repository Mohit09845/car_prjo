from pydantic import BaseModel, model_validator
from typing import List, Optional


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
    """ICE fuel tanks. Omit `cng_kg` unless you have a verified official figure."""

    petrol_litres: Optional[int] = None
    diesel_litres: Optional[int] = None
    cng_kg: Optional[float] = None


class ElectricSpecs(BaseModel):
    """Battery EV — use instead of `engine` / `fuel_tank` for pure electrics."""

    battery_capacity_kwh: List[float]
    range_km_arai_peak: Optional[int] = None
    peak_power_kw: Optional[float] = None


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
    dimensions: Dimensions
    safety: Safety
    colours: List[str]
    user_rating: float
    review_count: int

    engine: Optional[Engine] = None
    electric: Optional[ElectricSpecs] = None
    fuel_tank: Optional[FuelTank] = None

    @model_validator(mode="after")
    def ice_or_ev(self):
        if self.engine is None and self.electric is None:
            raise ValueError("Car must include either `engine` (ICE) or `electric` (EV).")
        if self.engine is not None and self.electric is not None:
            raise ValueError("Use either `engine` or `electric`, not both.")
        return self
