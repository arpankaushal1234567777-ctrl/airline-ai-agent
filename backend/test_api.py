import io
import os
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Import the app to test
from main import app

client = TestClient(app)


def generate_mock_pdf_bytes() -> bytes:
    """Generates a mock itinerary PDF in-memory using reportlab."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "FLIGHT ITINERARY - EMIRATES")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Passenger Name: Priya Singh")
    c.drawString(50, height - 120, "Booking Reference (PNR): EM848567")
    c.drawString(50, height - 140, "Class: First")

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


def generate_mock_image_bytes() -> bytes:
    """Generates a mock suitcase PNG image in-memory using Pillow."""
    buffer = io.BytesIO()
    img = Image.new("RGB", (600, 400), color=(240, 240, 240))
    d = ImageDraw.Draw(img)

    # Suitcase body
    d.rectangle([(200, 150), (400, 380)], fill=(30, 80, 150), outline=(20, 50, 100), width=5)
    d.rectangle([(270, 70), (330, 150)], outline=(100, 100, 100), width=8)  # Handle
    d.ellipse([(210, 360), (250, 400)], fill=(0, 0, 0))                      # Wheels
    d.ellipse([(350, 360), (390, 400)], fill=(0, 0, 0))

    # Text metadata specs
    d.text((50, 210), "- Category: Cabin Bag", fill=(0, 0, 0))
    d.text((50, 240), "- Size: 55 x 38 x 20 cm", fill=(0, 0, 0))
    d.text((50, 270), "- Weight: 8.0 kg", fill=(0, 0, 0))

    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()


def test_endpoints():
    print("=" * 60)
    print("RUNNING FASTAPI ENDPOINT TESTS")
    print("=" * 60)

    # 1. Test Root
    print("\n1. Testing GET / ...")
    res = client.get("/")
    assert res.status_code == 200
    print("Result:", res.json())

    # 2. Test Health
    print("\n2. Testing GET /health ...")
    res = client.get("/health")
    assert res.status_code == 200
    print("Result:", res.json())

    # 3. Test Reset API
    print("\n3. Testing POST /api/reset ...")
    res = client.post("/api/reset")
    assert res.status_code == 200
    assert res.json()["success"] is True
    print("Result:", res.json())

    # 4. Test Text-only Chat
    print("\n4. Testing POST /api/chat (Text-Only) ...")
    res = client.post(
        "/api/chat",
        data={"message": "What is the baggage fee for 30kg in economy class?"}
    )
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "tool_calls" in json_data
    assert len(json_data["tool_calls"]) > 0
    print("Result:", json_data)

    # 5. Test PDF Upload Chat
    print("\n5. Testing POST /api/chat (PDF Upload) ...")
    pdf_bytes = generate_mock_pdf_bytes()
    res = client.post(
        "/api/chat",
        data={"message": "What is my passenger name, PNR, and travel class based on this itinerary PDF?"},
        files={"file": ("itinerary.pdf", pdf_bytes, "application/pdf")}
    )
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "tool_calls" in json_data
    assert "rag_sources" in json_data
    print("Result:", json_data)

    # 6. Test Image Upload Chat
    print("\n6. Testing POST /api/chat (Image Upload) ...")
    img_bytes = generate_mock_image_bytes()
    res = client.post(
        "/api/chat",
        data={"message": "Can I carry this suitcase as cabin baggage in economy class?"},
        files={"file": ("suitcase.png", img_bytes, "image/png")}
    )
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["success"] is True
    assert "tool_calls" in json_data
    assert len(json_data["tool_calls"]) > 0
    print("Result:", json_data)

    print("\n" + "=" * 60)
    print("✅ ALL FASTAPI REST API TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    test_endpoints()
