from app.llm.chatbot import AirlineChatbot


def main():

    chatbot = AirlineChatbot()

    print("=" * 50)
    print("✈️ Airline AI Customer Support Agent")
    print("Type 'exit' to quit.")
    print("=" * 50)

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = chatbot.ask(question)

        print(f"\nAI: {answer}")


if __name__ == "__main__":
    main()