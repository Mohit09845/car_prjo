from pydantic import BaseModel, model_validator, Field
from typing import List, Optional, Literal

CarTransmission = Literal["Manual", "Automatic", "CVT"]
FuelType = Literal["Petrol", "CNG", "Diesel", "Hybrid", "Electric"]


class PriceRange(BaseModel):
    min_ex_showroom: int
    max_ex_showroom: int

    @model_validator(mode="after")
    def check_range(self):
        if self.min_ex_showroom > self.max_ex_showroom:
            raise ValueError("min_ex_showroom must be <= max_ex_showroom")
        return self


class EngineOption(BaseModel):
    displacement_cc: int
    cylinders: int
    fuel_type: FuelType


class Engine(BaseModel):
    options: List[EngineOption]
    transmissions: List[CarTransmission]


class FuelTank(BaseModel):
    petrol_litres: Optional[float] = None
    diesel_litres: Optional[float] = None
    cng_litres: Optional[float] = None

    @model_validator(mode="after")
    def at_least_one_fuel(self):
        if all(v is None for v in [self.petrol_litres, self.diesel_litres, self.cng_litres]):
            raise ValueError("FuelTank must specify at least one fuel capacity.")
        return self


class ElectricSpecs(BaseModel):
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
    has_abs: bool = Field(alias="abs")
    has_ebd: bool = Field(alias="ebd")
    has_esc: bool = Field(alias="esc")
    hill_assist: bool
    isofix: bool
    ncap_stars: Optional[int] = None


class Car(BaseModel):
    make: str
    model: str
    car_type: str = Field(alias="type")
    price_range_inr: PriceRange
    dimensions: Dimensions
    safety: Safety
    colours: List[str]
    user_rating: float = Field(..., ge=0.0, le=5.0)
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
