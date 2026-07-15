import os
from PIL import Image, ImageDraw

from app.llm.chatbot import AirlineChatbot


def generate_mock_suitcase_image(output_path: str):
    """Generates a mock suitcase PNG image with spec text."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (600, 400), color=(240, 240, 240))
    d = ImageDraw.Draw(img)

    # Suitcase outline
    d.rectangle([(200, 150), (400, 380)], fill=(30, 80, 150), outline=(20, 50, 100), width=5)
    d.rectangle([(270, 70), (330, 150)], outline=(100, 100, 100), width=8)  # Handle
    d.ellipse([(210, 360), (250, 400)], fill=(0, 0, 0))                      # Wheels
    d.ellipse([(350, 360), (390, 400)], fill=(0, 0, 0))

    # Text spec labels
    d.text((50, 180), "LUGGAGE SPECS:", fill=(0, 0, 0))
    d.text((50, 210), "- Category: Cabin Bag", fill=(0, 0, 0))
    d.text((50, 240), "- Size: 55 x 38 x 20 cm", fill=(0, 0, 0))
    d.text((50, 270), "- Weight: 8.0 kg", fill=(0, 0, 0))

    img.save(output_path)
    print(f"[TEST SETUP] Generated mock suitcase image at: {output_path}")


def generate_mock_boarding_pass(output_path: str):
    """Generates a mock Emirates boarding pass PNG image with details."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (600, 250), color=(255, 235, 235))  # Light red tint
    d = ImageDraw.Draw(img)

    # Boarding pass headers/borders
    d.rectangle([(20, 20), (580, 230)], outline=(180, 50, 50), width=4)
    d.line([(420, 20), (420, 230)], fill=(180, 50, 50), width=2)  # Perforated line

    # Text details
    d.text((40, 40), "EMIRATES BOARDING PASS", fill=(180, 0, 0))
    d.text((40, 80), "Passenger: VIKRAM PATEL", fill=(0, 0, 0))
    d.text((40, 110), "Flight: EK408", fill=(0, 0, 0))
    d.text((40, 140), "Route: Bangkok (BKK) to Singapore (SIN)", fill=(0, 0, 0))
    d.text((40, 170), "Class: First Class", fill=(0, 0, 0))
    d.text((40, 200), "Seat: 39F", fill=(0, 0, 0))

    # Stub (Right side)
    d.text((440, 40), "FLIGHT: EK408", fill=(0, 0, 0))
    d.text((440, 70), "SEAT: 39F", fill=(0, 0, 0))
    d.text((440, 110), "PNR: EM455916", fill=(0, 0, 0))

    img.save(output_path)
    print(f"[TEST SETUP] Generated mock boarding pass image at: {output_path}")


def generate_mock_passport(output_path: str):
    """Generates a mock passport details page PNG image."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img = Image.new("RGB", (600, 350), color=(235, 245, 255))  # Light blue tint
    d = ImageDraw.Draw(img)

    # Passport details outline
    d.rectangle([(30, 30), (570, 320)], outline=(50, 100, 150), width=4)
    
    # Photo placeholder
    d.rectangle([(60, 70), (210, 250)], fill=(200, 200, 200), outline=(100, 100, 100))
    d.text((90, 150), "[ PHOTO ]", fill=(50, 50, 50))

    # Text details
    d.text((250, 50), "REPUBLIC OF INDIA / PASSPORT", fill=(20, 50, 100))
    d.text((250, 90), "Surname: SINGH", fill=(0, 0, 0))
    d.text((250, 120), "Given Name: PRIYA", fill=(0, 0, 0))
    d.text((250, 150), "Nationality: INDIAN", fill=(0, 0, 0))
    d.text((250, 180), "Passport No: J1234567", fill=(0, 0, 0))
    d.text((250, 210), "Date of Birth: 15-08-1998", fill=(0, 0, 0))
    d.text((250, 240), "Gender: F", fill=(0, 0, 0))

    img.save(output_path)
    print(f"[TEST SETUP] Generated mock passport image at: {output_path}")


def run_tests():
    img_dir = "data/uploads"
    suitcase_path = os.path.join(img_dir, "mock_suitcase.png")
    boarding_pass_path = os.path.join(img_dir, "mock_boarding_pass.png")
    passport_path = os.path.join(img_dir, "mock_passport.png")

    # Generate all three mock images
    generate_mock_suitcase_image(suitcase_path)
    generate_mock_boarding_pass(boarding_pass_path)
    generate_mock_passport(passport_path)

    chatbot = AirlineChatbot()

    # ============================================================
    # TEST 1: Suitcase & Luggage check
    # ============================================================
    print("\n" + "=" * 60)
    print("TEST 1: SUITCASE ANALYSIS")
    print("=" * 60)
    q1 = "Can I carry this suitcase as cabin baggage in economy class?"
    print(f"\nUser: {q1}")
    ans1 = chatbot.ask(q1, file_path=suitcase_path)
    print(f"AI: {ans1['answer']}")

    # Upgrade follow up
    q1_follow = "What if I upgrade to Premium Economy?"
    print(f"\nUser: {q1_follow}")
    ans1_follow = chatbot.ask(q1_follow)
    print(f"AI: {ans1_follow['answer']}")

    # Clear memory for next tests
    chatbot.reset()

    # ============================================================
    # TEST 2: Boarding Pass OCR
    # ============================================================
    print("\n" + "=" * 60)
    print("TEST 2: BOARDING PASS ANALYSIS")
    print("=" * 60)
    q2 = "Extract my passenger name, PNR, flight number, and seat from this boarding pass image."
    print(f"\nUser: {q2}")
    ans2 = chatbot.ask(q2, file_path=boarding_pass_path)
    print(f"AI: {ans2['answer']}")

    # Tool execution follow up (check status of flight extracted from image)
    q2_follow = "What is the status of my flight?"
    print(f"\nUser: {q2_follow}")
    ans2_follow = chatbot.ask(q2_follow)
    print(f"AI: {ans2_follow['answer']}")

    chatbot.reset()

    # ============================================================
    # TEST 3: Passport OCR
    # ============================================================
    print("\n" + "=" * 60)
    print("TEST 3: PASSPORT ANALYSIS")
    print("=" * 60)
    q3 = "What is the passenger name and passport number shown in this passport photo?"
    print(f"\nUser: {q3}")
    ans3 = chatbot.ask(q3, file_path=passport_path)
    print(f"AI: {ans3['answer']}")

    chatbot.reset()

    # Clean up test files
    for path in [suitcase_path, boarding_pass_path, passport_path]:
        if os.path.exists(path):
            os.remove(path)
    print("\n[TEST CLEANUP] Removed all mock test images.")


if __name__ == "__main__":
    run_tests()
