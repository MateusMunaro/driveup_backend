from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from models.models import *

class Coordinates(BaseModel):
    latitude: float
    longitude: float

class StgRidesSchema(BaseModel):
    ride_id: int
    ride_date: Optional[str] = None
    driver_name: str
    start_time: str
    end_time: str
    duration_seconds: int
    distance_km: float
    hotel_name: Optional[str] = None
    pax_name: Optional[str] = None
    client_name: str
    total_value: Optional[float] = None
    car_model: Optional[str] = None
    payment_method: Optional[str] = None
    observation: Optional[str] = None
    indication_source: Optional[str] = None
    origin_coords: Optional[Coordinates] = None
    destination_coords: Optional[Coordinates] = None
    positions: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True  # Habilita a compatibilidade com ORMs (como SQLAlchemy)

class DimHotelsSchema(BaseModel):
    hotel_id: Optional[int]
    hotel_name: str
    address: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]

    class Config:
        from_attributes = True  # Habilita a compatibilidade com ORMs (como SQLAlchemy)

class DimClientsSchema(BaseModel):
    client_id: int
    client_name: str
    contact_info: Optional[str]
    client_type: Optional[str]
    creation_date: Optional[datetime]

    class Config:
        from_attributes = True

class DimCarsSchema(BaseModel):
    car_id: int
    car_model: str
    car_plate: Optional[str] = None
    car_year: Optional[int] = None
    capacity: Optional[int] = None
    fuel_type: Optional[str]
    creation_date: Optional[datetime]

    class Config:
        from_attributes = True

class DimDriversSchema(BaseModel):
    driver_id: int
    driver_name: str
    contact_info: Optional[str]
    driver_role: Optional[str]
    active_status: Optional[bool]
    hire_date: Optional[date]
    creation_date: Optional[datetime]

    class Config:
        from_attributes = True

class DriverAuthenticationSchema(BaseModel):
    driver_id: int
    hash_password: str
    last_login: Optional[datetime]

    class Config:
        from_attributes = True

class DimCompaniesSchema(BaseModel):
    company_id: int
    company_name: str
    contact_info: Optional[str]
    service_type: Optional[str]
    headquarters_city: Optional[str]
    creation_date: Optional[datetime]

    class Config:
        from_attributes = True

class FctRidesSchema(BaseModel):
    sk_ride: int
    sk_hotel: Optional[int]
    sk_client: Optional[int]
    sk_car: Optional[int]
    sk_driver: Optional[int]
    ride_date: date
    origin: str
    destination: str
    total_value: float
    payment_method: Optional[str]
    total_billed: Optional[float]
    observation: Optional[str]
    creation_date: Optional[datetime]

    class Config:
        from_attributes = True

class DimPricingSchema(BaseModel):
    pricing_id: int
    ride_type: Optional[str]
    base_rate: Optional[float]
    per_km_rate: Optional[float]
    surge_multiplier: Optional[float]
    effective_date: Optional[date]
    expiration_date: Optional[date]

    class Config:
        from_attributes = True

class DimIndicationsSchema(BaseModel):
    sk_indication: int
    indication_name: str

    class Config:
        from_attributes = True

class MonthlyRidesSchema(BaseModel):
    data: date
    total_rides: int

    class Config:
        from_attributes = True

class DriverSchema(BaseModel):
    driver_id: Optional[int] = None
    driver_name: str
    contact_info: Optional[str] = None
    driver_role: Optional[str] = None
    active_status: Optional[bool] = None
    hire_date: Optional[date] = None
    password: Optional[str] = None
    creation_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class RankingSchema(BaseModel):
    driver_id: int = None
    driver_name: str = None
    ride_count: Optional[int] = None

