"""
Quick manual test for AirlineChatbot function-calling + RAG fallback.

Run from the backend/ directory:
    python test_chatbot_tools.py
"""

from app.llm.chatbot import AirlineChatbot


def run(bot, label, question):
    print(f"\n{'='*60}")
    print(f"[{label}] Q: {question}")
    print('=' * 60)
    try:
        answer = bot.ask(question)
        print(f"A: {answer}")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")


def main():

    bot = AirlineChatbot()

    # --- Should trigger tool calls ---
    run(bot, "TOOL: search_flights", "Find me flights from Dubai to London")
    run(bot, "TOOL: baggage_fee", "What's the extra baggage fee for 30kg in economy class?")
    run(bot, "TOOL: nearest_airport", "What's the nearest airport to Mumbai?")
    run(bot, "TOOL: cancel_booking", "Cancel my booking EM123456")
    run(bot, "TOOL: airline_lookup", "What is the ICAO code for Emirates?")
    run(bot, "TOOL: aircraft_lookup", "Tell me about the Airbus A380-800")

    # --- Should fall back to RAG (no matching tool) ---
    run(bot, "RAG: baggage policy", "What is your baggage allowance policy for international flights?")
    run(bot, "RAG: refund", "What is your refund policy for cancelled tickets?")


if __name__ == "__main__":
    main()