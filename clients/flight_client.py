import os
import requests
from dotenv import load_dotenv

load_dotenv()


class FlightClient:

  def __init__(self):
    # Pulls the API key from environment variables (local .env or GitHub Actions Secrets)
    self.api_key = os.getenv("FLIGHT_API_KEY", "mock_key")
    # Replace with the actual host endpoint of the RapidAPI provider you subscribe to
    self.api_host = os.getenv("FLIGHT_API_HOST", "skyscanner-api-example.p.rapidapi.com")

  def search_flights(self, origin: str, destination: str, departure_date: str) -> list[dict]:
    """Fetches real-time flight offers using RapidAPI,

    falling back to synchronized mock records if credits run out or the network fails.
    """
    # 1. Attempt Real-Time API Call if a valid API key is present
    if self.api_key and self.api_key != "mock_key":
      try:
        url = f"https://{self.api_host}/v2/flights/search"
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.api_host,
        }
        params = {
            "origin": origin,
            "destination": destination,
            "date": departure_date,
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
          data = response.json()
          live_flights = data.get("flights", [])
          if live_flights:
            print(" Success: Fetched live data from RapidAPI!")
            return live_flights
      except Exception as e:
        print(f"⚠️ Live API call failed or rate-limited ({e}). Falling back to mock data.")

    # 2. Graceful Mock Fallback (Guarantees 100% uptime for tests and CI/CD)
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
        {
            "flight_id": "FL-104",
            "origin": "YYC",
            "destination": "AMD",
            "airline": "WestJet",
            "price_cad": 1399.00,
            "currency": "CAD",
            "departure_date": "2026-12-12",
            "booking_url": "https://example.com/book/104",
        },
    ]

    # Filter mock records matching the requested parameters
    filtered_flights = [
        f
        for f in mock_flight_database
        if f["origin"] == origin
        and f["destination"] == destination
        and f["departure_date"] == departure_date
    ]

    return filtered_flights