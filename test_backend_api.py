import sys
import asyncio
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from app import (
    health_check,
    get_sample_images,
    predict_disease,
    get_disease_details,
    list_all_diseases,
    plant_health_chat,
    get_history,
    ChatRequest
)
from fastapi import UploadFile

async def run_tests():
    print("1. Testing health_check()...")
    health = health_check()
    print("   Health:", health["status"], "| Classes count:", health["supported_classes_count"])
    assert health["status"] == "healthy"
    assert health["supported_classes_count"] == 115

    print("2. Testing get_sample_images()...")
    samples = get_sample_images()
    sample_list = samples["samples"]
    print(f"   Returned {len(sample_list)} samples.")
    assert len(sample_list) >= 10

    print("3. Testing predict_disease() with sample leaf...")
    sample_path = Path("samples") / "tomato_early_blight.jpg"
    with open(sample_path, "rb") as f:
        file_bytes = f.read()
    
    upload_file = UploadFile(
        file=io.BytesIO(file_bytes),
        filename="tomato_early_blight.jpg",
        headers={"content-type": "image/jpeg"}
    )
    
    pred = await predict_disease(upload_file)
    print("   Prediction:", pred["disease"], "| Confidence:", pred["confidence_percentage"], "| Latency:", pred["latency_ms"], "ms")
    assert pred["disease"] == "Tomato Early Blight"
    assert pred["crop"] == "Tomato"

    print("4. Testing get_disease_details()...")
    details = get_disease_details("Tomato_Early_Blight")
    print("   Disease info loaded for:", details["disease_name"])
    assert details["crop"] == "Tomato"

    print("5. Testing list_all_diseases()...")
    catalog = list_all_diseases()
    diseases_dict = catalog.get("diseases", {})
    print("   Total catalog diseases:", len(diseases_dict))
    assert len(diseases_dict) == 115

    print("6. Testing plant_health_chat() (AI Agent)...")
    chat_req = ChatRequest(
        message="What is the recommended organic spray recipe?",
        context={
            "disease": pred["disease"],
            "crop": pred["crop"],
            "disease_id": pred["disease_id"],
            "severity": pred["severity"]
        }
    )
    chat_resp = plant_health_chat(chat_req)
    print("   Agent response received! Context:", chat_resp["disease_context"])
    print("   Follow-ups suggested:", len(chat_resp["suggested_follow_ups"]))
    assert len(chat_resp["suggested_follow_ups"]) > 0

    print("7. Testing get_history()...")
    hist = get_history()
    print("   History log count:", hist["total"])
    assert hist["total"] > 0

    print("\n🎉 ALL BACKEND API ENDPOINT HANDLERS ARE FULLY OPERATIONAL AND PASSING!")

if __name__ == "__main__":
    asyncio.run(run_tests())
