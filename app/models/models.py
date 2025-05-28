from sqlalchemy import Column, Integer, String, Date, Text, Numeric, TIMESTAMP, func, Boolean, ForeignKey, Float, DateTime
from app.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class StgRides(Base):
    __tablename__ = "stg_rides"

    ride_id = Column(Integer, primary_key=True, autoincrement=True)  # serial4
    client_name = Column(String(255), nullable=False)  # NOT NULL
    hotel_name = Column(String(255), nullable=True)
    driver_name = Column(String(255), nullable=True)
    car_model = Column(String(255), nullable=True)
    payment_method = Column(String(100), nullable=True)
    total_value = Column(Float, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)  # timestamptz NOT NULL
    end_time = Column(DateTime(timezone=True), nullable=False)  # timestamptz NOT NULL
    duration_seconds = Column(Integer, nullable=False)  # NOT NULL
    distance_km = Column(Float, nullable=False)  # NOT NULL
    origin_latitude = Column(Float, nullable=True)
    origin_longitude = Column(Float, nullable=True)
    destination_latitude = Column(Float, nullable=True)
    destination_longitude = Column(Float, nullable=True)
    observation = Column(Text, nullable=True)
    indication_source = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)  # CURRENT_TIMESTAMP

    positions = relationship("DimPositionModel", back_populates="ride")

class DimPositionModel(Base):
    __tablename__ = "dim_positions"

    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("stg_rides.ride_id"))
    latitude = Column(Float)
    longitude = Column(Float)
    accuracy = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    ride = relationship("StgRides", back_populates="positions")
    

class DimHotels(Base):
    __tablename__ = 'dim_hotels'

    hotel_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_name = Column(String(200), unique=True, nullable=False)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(50))
    country = Column(String(50))


class DimClients(Base):
    __tablename__ = 'dim_clients'

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    client_name = Column(String(200), unique=True, nullable=False)
    contact_info = Column(Text)
    client_type = Column(String(50))
    creation_date = Column(TIMESTAMP, server_default=func.now())


class DimCars(Base):
    __tablename__ = 'dim_cars'

    car_id = Column(Integer, primary_key=True, autoincrement=True)
    car_model = Column(String(100), unique=True, nullable=False)
    car_plate = Column(String(20), nullable=False)
    car_year = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    fuel_type = Column(String(50))
    creation_date = Column(TIMESTAMP, server_default=func.now())


class DimDrivers(Base):
    __tablename__ = 'dim_drivers'

    driver_id = Column(Integer, primary_key=True, autoincrement=True)
    driver_name = Column(String(200), unique=True, nullable=False)
    contact_info = Column(Text)
    driver_role = Column(String(255))
    active_status = Column(Boolean, default=True)
    hire_date = Column(Date)
    creation_date = Column(TIMESTAMP, server_default=func.now())


class DriverAuthentication(Base):
    __tablename__ = 'driver_authentication'

    driver_id = Column(Integer, ForeignKey('dim_drivers.driver_id'), primary_key=True)
    hash_password = Column(String(255), nullable=False)
    last_login = Column(TIMESTAMP, server_default=func.now())


class DimCompanies(Base):
    __tablename__ = 'dim_companies'

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    contact_info = Column(Text)
    service_type = Column(String(100))
    headquarters_city = Column(String(100))
    creation_date = Column(TIMESTAMP, server_default=func.now())


class FctRides(Base):
    __tablename__ = 'fct_rides'

    ride_id = Column(Integer, primary_key=True, autoincrement=True)
    hotel_id = Column(Integer, ForeignKey('dim_hotels.hotel_id'))
    client_id = Column(Integer, ForeignKey('dim_clients.client_id'))
    car_id = Column(Integer, ForeignKey('dim_cars.car_id'))
    driver_id = Column(Integer, ForeignKey('dim_drivers.driver_id'))
    ride_date = Column(Date, nullable=False)
    origin_latitude = Column(Float, nullable=False)
    origin_longitude = Column(Float, nullable=False)
    destination_latitude = Column(Float, nullable=False)
    destination_longitude = Column(Float, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    total_value = Column(Numeric(18, 2), nullable=True)
    payment_method = Column(String(50))
    creation_date = Column(TIMESTAMP, server_default=func.now())


class DimPricing(Base):
    __tablename__ = 'dim_pricing'

    pricing_id = Column(Integer, primary_key=True, autoincrement=True)
    ride_type = Column(String(50))
    base_rate = Column(Numeric(10, 2))
    per_km_rate = Column(Numeric(10, 2))
    surge_multiplier = Column(Numeric(3, 2))
    effective_date = Column(Date)
    expiration_date = Column(Date)


class DimIndications(Base):
    __tablename__ = 'dim_indications'

    sk_indication = Column(Integer, primary_key=True, autoincrement=True)
    indication_name = Column(String(100), unique=True, nullable=False)