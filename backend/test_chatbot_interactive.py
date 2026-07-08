from app.llm.chatbot import AirlineChatbot


def main():

    chatbot = AirlineChatbot()

    print("=" * 50)
    print("✈️ Airline AI Customer Support Agent (with tools)")
    print("Type 'exit' to quit.")
    print("=" * 50)
    print("Try things like:")
    print("  - Find me flights from Dubai to London")
    print("  - What's the baggage fee for 30kg in economy?")
    print("  - Cancel my booking EM123456")
    print("  - What is your refund policy?")
    print("=" * 50)

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        try:
            answer = chatbot.ask(question)
            print(f"\nAI: {answer}")

        except Exception as e:
            print(f"\n[ERROR] {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()