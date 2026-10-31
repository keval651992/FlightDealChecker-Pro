from typing import Optional
from pydantic import BaseModel, Field


class FlightOfferSchema(BaseModel):
  flight_id: str
  origin: str = Field(..., min_length=3, max_length=3)
  destination: str = Field(..., min_length=3, max_length=3)
  airline: str
  price_cad: float = Field(..., gt=0)
  currency: str = "CAD"
  departure_date: str
  booking_url: Optional[str] = None