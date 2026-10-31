import pytest
from clients.flight_client import FlightClient
from models.flight_schemas import FlightOfferSchema


@pytest.fixture
def flight_client():
  return FlightClient()


@pytest.mark.parametrize("origin, destination, target_date", [("YYC", "AMD","2026-12-12"),],)
def test_flight_deals_contract_and_budget(flight_client, origin, destination, target_date):
    
  # 1. Fetch raw flight data
  raw_offers = flight_client.search_flights(origin, destination,target_date)
  assert len(raw_offers) > 0, "No flight offers returned from search."

  target_budget_cad = 1500.00  # Your maximum desired price threshold
  deal_found = False

  for raw_offer in raw_offers:
    # 2. Validate response structure using Pydantic schema contract
    validated_offer = FlightOfferSchema(**raw_offer)

    assert validated_offer.origin == origin
    assert validated_offer.destination == destination
    assert validated_offer.departure_date == target_date
    
    print(
        f"Date: {validated_offer.departure_date}"
        f"Checked {validated_offer.airline}: ${validated_offer.price_cad}"
        f" {validated_offer.currency}"
    )

    # 3. Check if any flight meets your target budget deal threshold
    if validated_offer.price_cad <= target_budget_cad:
      deal_found = True

  # Assert that at least one flight met your criteria
  assert (
      deal_found
  ), f"No flights found under your target budget of ${target_budget_cad} CAD."