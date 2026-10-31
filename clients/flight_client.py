import os
import requests
from dotenv import load_dotenv

load_dotenv()


class FlightClient:

  def __init__(self):
    self.api_key = os.getenv("FLIGHT_API_KEY", "mock_key")
    self.base_url = os.getenv(
        "FLIGHT_API_URL", "https://api.example-flights.com/v1"
    )

  def search_flights(self, origin: str, destination: str) -> list[dict]:
    """Fetches flight offers.

    Falls back to structured mock data if live API is unavailable.
    """
    try:
      # Live API integration attempt (e.g., Skyscanner / Amadeus / RapidAPI)
      headers = {"X-Api-Key": self.api_key}
      response = requests.get(
          f"{self.base_url}/search",
          params={"origin": origin, "destination": destination},
          headers=headers,
          timeout=5,
      )
      if response.status_code == 200:
        return response.json()
    except Exception:
      pass

    # Simulated Mock Flight Deals (e.g., tracking Calgary (YYC) to Ahmedabad (AMD) or regional trips)
    mock_flight_database = [
        {
            "flight_id": "FL-101",
            "origin": "YYC",
            "destination": "AMD",
            "airline": "Air Canada",
            "price_cad": 1450.00,
            "currency": "CAD",
            "departure_date": "2026-12-15",
            "booking_url": "https://example.com/book/101",
        },
        {
            "flight_id": "FL-102",
            "origin": "YYC",
            "destination": "AMD",
            "airline": "Lufthansa",
            "price_cad": 1320.50,
            "currency": "CAD",
            "departure_date": "2026-12-15",
            "booking_url": "https://example.com/book/102",
        },
    ]

    return mock_flight_database