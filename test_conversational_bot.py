import urllib.request
import json
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8000/chat"

test_queries = [
    {
        "name": "1. What Questions Can I Ask?",
        "payload": {
            "message": "what are the question we ask about a plant",
            "context": None
        },
        "must_contain": ["AI Agronomist", "Diagnosis & Leaf Symptoms", "Organic & Homemade DIY Remedies", "Watering, Soil"]
    },
    {
        "name": "2. Leaf Symptoms & Yellowing Diagnosis",
        "payload": {
            "message": "Why are my leaves turning yellow, brown, and curling?",
            "context": None
        },
        "must_contain": ["Overwatering", "Chlorosis", "Nitrogen"]
    },
    {
        "name": "3. Watering & Root Rot",
        "payload": {
            "message": "How often should I water and how to prevent root rot?",
            "context": None
        },
        "must_contain": ["Finger Test", "Hydrogen Peroxide", "drainage"]
    },
    {
        "name": "4. Organic Spray & Neem Oil",
        "payload": {
            "message": "Can you give me a homemade organic spray recipe?",
            "context": {"disease": "Tomato Early Blight", "crop": "Tomato", "severity": "Moderate"}
        },
        "must_contain": ["Baking Soda", "Neem Oil", "Castile"]
    },
    {
        "name": "5. Harvest Safety & Edibility",
        "payload": {
            "message": "Can I safely eat tomatoes from this plant?",
            "context": {"disease": "Tomato Early Blight", "crop": "Tomato", "severity": "Moderate"}
        },
        "must_contain": ["SAFE TO EAT", "Pre-Harvest Interval"]
    },
    {
        "name": "6. Natural Pest Control",
        "payload": {
            "message": "How do I get rid of aphids and spider mites naturally?",
            "context": None
        },
        "must_contain": ["Insecticidal Soap", "Neem", "Ladybugs"]
    }
]

print("=== STARTING CONVERSATIONAL BOT INTELLIGENCE TEST ===")
for test in test_queries:
    print(f"\nTesting: {test['name']}")
    req_data = json.dumps(test["payload"]).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode("utf-8"))
        ans = data["answer"]
        print(f"Answer snippet: {ans[:150]}...")
        print(f"Suggested follow-ups: {data.get('suggested_follow_ups')}")
        for word in test["must_contain"]:
            assert word.lower() in ans.lower(), f"Missing expected keyword '{word}' in answer!"
        print(f"   ✅ Passed: {test['name']}")

print("\n========================================================")
print("🎉 ALL CONVERSATIONAL BOT INTELLIGENCE TESTS PASSED 100%!")
print("========================================================")
