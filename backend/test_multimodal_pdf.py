from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

from app.llm.chatbot import AirlineChatbot


def generate_itinerary_pdf(output_path: str):
    """
    Generates a mock Emirates itinerary PDF using reportlab.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "FLIGHT ITINERARY - EMIRATES")

    # Details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Passenger Name: Priya Singh")
    c.drawString(50, height - 120, "Booking Reference (PNR): EM848567")
    c.drawString(50, height - 140, "Flight Number: EK257")
    c.drawString(50, height - 160, "Route: Hyderabad (HYD) to Delhi (DEL)")
    c.drawString(50, height - 180, "Class: First")
    c.drawString(50, height - 200, "Seat: 38B")
    c.drawString(50, height - 220, "Status: Confirmed")

    # Baggage Info
    c.drawString(50, height - 260, "Baggage Details:")
    c.drawString(50, height - 280, "- Checked Baggage Allowance: 50 kg")
    c.drawString(50, height - 300, "- Actual Checked Baggage Weight: 55 kg")

    c.save()
    print(f"[TEST SETUP] Generated mock PDF itinerary at: {output_path}")


def run_tests():
    pdf_dir = "data/uploads"
    pdf_path = os.path.join(pdf_dir, "test_itinerary.pdf")
    
    # 1. Setup mock PDF
    generate_itinerary_pdf(pdf_path)

    # 2. Init chatbot
    chatbot = AirlineChatbot()

    print("=" * 60)
    print("RUNNING PDF MULTIMODAL VERIFICATION TESTS")
    print("=" * 60)

    # Turn 1: Ask question with PDF file_path
    q1 = "Can you extract my passenger name, PNR, flight number, and travel class from the attached itinerary?"
    print(f"\nUser: {q1}")
    ans1 = chatbot.ask(q1, file_path=pdf_path)
    print(f"AI: {ans1['answer']}")

    # Turn 2: Follow-up question without passing file_path (verifying memory and tool usage)
    q2 = "According to the ticket details, my baggage weight is 55kg. Calculate the baggage fee for me."
    print(f"\nUser: {q2}")
    ans2 = chatbot.ask(q2)
    print(f"AI: {ans2['answer']}")

    # Turn 3: Verify context safety by checking saved messages in history
    print("\n" + "=" * 60)
    print("VERIFYING MEMORY CONTEXT SAFETY & PERSISTENCE")
    print("=" * 60)
    
    pdf_persists = False
    total_memory_length = 0
    
    for msg in chatbot.messages:
        total_memory_length += len(msg.content)
        if "attached a PDF document" in msg.content or "FLIGHT ITINERARY" in msg.content:
            pdf_persists = True
            
    print(f"Total session memory length: {total_memory_length} characters.")
    
    if pdf_persists and total_memory_length < 6000:
        print("\n✅ SUCCESS: PDF text correctly persisted for follow-up questions, and memory size is safely bounded.")
    else:
        if not pdf_persists:
            print("\n❌ FAILURE: PDF text was lost from memory history.")
        if total_memory_length >= 6000:
            print(f"\n❌ FAILURE: Memory context size is too large ({total_memory_length} chars).")

    # Clean up test file
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        print("\n[TEST CLEANUP] Removed test itinerary PDF.")


if __name__ == "__main__":
    run_tests()
