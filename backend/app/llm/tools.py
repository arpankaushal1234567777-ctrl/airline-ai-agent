"""
LangChain tool wrappers around app/functions/*.py

Each function is wrapped with the @tool decorator so it can be bound
to the LLM via llm.bind_tools([...]) and invoked automatically when
the model decides a function call is needed.
"""

from langchain_core.tools import tool

from app.functions.search_flights import search_flights
from app.functions.baggage_fee import calculate_baggage_fee
from app.functions.cancel_booking import cancel_booking
from app.functions.nearest_airport import nearest_airport
from app.functions.aircraft_lookup import find_aircraft
from app.functions.airline_lookup import find_airline
from app.functions.airport_lookup import find_airport
# from app.functions.refund_policy import get_refund_policy  # add once written
# from app.functions.flight_status import check_flight_status  # not built yet
# from app.functions.weather import get_weather  # not built yet


@tool
def search_flights_tool(origin: str, destination: str) -> list:
    """
    Search for Emirates flights between two cities.

    Args:
        origin: Departure city name (e.g. "Dubai").
        destination: Arrival city name (e.g. "London").
    """
    return search_flights(origin, destination)


@tool
def calculate_baggage_fee_tool(travel_class: str, baggage_weight: float) -> dict:
    """
    Calculate excess baggage fees for a given travel class and weight.

    Args:
        travel_class: One of "Economy", "Premium Economy", "Business", "First".
        baggage_weight: Total baggage weight in kilograms.
    """
    return calculate_baggage_fee(travel_class, baggage_weight)


@tool
def cancel_booking_tool(pnr: str) -> dict:
    """
    Cancel a booking using its PNR (booking reference).

    Args:
        pnr: The 8-character PNR code, e.g. "EM123456".
    """
    return cancel_booking(pnr)


@tool
def nearest_airport_tool(city: str) -> dict:
    """
    Find the nearest airport to a given city.

    Args:
        city: City name, e.g. "Mumbai".
    """
    return nearest_airport(city)


@tool
def find_aircraft_tool(query: str) -> list:
    """
    Look up aircraft details by name, IATA, or ICAO code.

    Args:
        query: Aircraft name or code, e.g. "Airbus A380-800" or "388".
    """
    return find_aircraft(query)


@tool
def find_airline_tool(query: str) -> list:
    """
    Look up airline details by name, IATA, or ICAO code.

    Args:
        query: Airline name or code, e.g. "Emirates" or "EK".
    """
    return find_airline(query)


@tool
def find_airport_tool(city: str) -> list:
    """
    Look up airport details (name, IATA, ICAO, country) for a city.

    Args:
        city: City name, e.g. "Dubai".
    """
    return find_airport(city)


# Collect all tools here so chatbot.py just imports this one list.
ALL_TOOLS = [
    search_flights_tool,
    calculate_baggage_fee_tool,
    cancel_booking_tool,
    nearest_airport_tool,
    find_aircraft_tool,
    find_airline_tool,
    find_airport_tool,
]

TOOLS_BY_NAME = {t.name: t for t in ALL_TOOLS}