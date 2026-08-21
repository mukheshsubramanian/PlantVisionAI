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
    register_user,
    login_user,
    get_current_profile,
    logout_user,
    predict_disease,
    get_history,
    plant_health_chat,
    UserRegisterRequest,
    UserLoginRequest,
    ChatRequest
)
from auth_service import get_auth_service
from fastapi import UploadFile

async def test_complete_system():
    print("==================================================")
    print("PLANTVISION AI - COMPREHENSIVE END-TO-END SUITE")
    print("==================================================")

    auth_svc = get_auth_service()
    test_user = "farmer_john"
    test_email = "john@greenvalleys.org"
    test_pass = "Harvest2026Secure!"

    # Clean up test user if exists
    for uid in list(auth_svc.users.keys()):
        if auth_svc.users[uid]["username"] == test_user or auth_svc.users[uid]["email"] == test_email:
            del auth_svc.users[uid]
    auth_svc._save_users()

    # 1. Register
    print("1. Testing Registration Endpoint (/auth/register)...")
    reg_req = UserRegisterRequest(
        username=test_user,
        email=test_email,
        password=test_pass,
        full_name="John Henderson"
    )
    reg_resp = register_user(reg_req)
    token = reg_resp["token"] if isinstance(reg_resp, dict) else reg_resp.token
    user_name = reg_resp["user"]["full_name"] if isinstance(reg_resp, dict) else reg_resp.user.full_name
    print(f"   Registered successfully: {user_name}, Token: {token[:12]}...")
    assert (reg_resp["user"]["username"] if isinstance(reg_resp, dict) else reg_resp.user.username) == test_user

    # 2. Login
    print("2. Testing Login Endpoint (/auth/login)...")
    login_req = UserLoginRequest(
        username_or_email=test_email,
        password=test_pass
    )
    login_resp = login_user(login_req)
    token = login_resp["token"] if isinstance(login_resp, dict) else login_resp.token
    login_user_name = login_resp["user"]["full_name"] if isinstance(login_resp, dict) else login_resp.user.full_name
    print(f"   Logged in: {login_user_name}, Token: {token[:12]}...")
    assert token is not None

    # 3. Profile /auth/me
    print("3. Testing Profile Validation (/auth/me)...")
    me_resp = get_current_profile(authorization=f"Bearer {token}")
    print(f"   Current User: {me_resp['user']['full_name']} | Email: {me_resp['user']['email']}")
    assert me_resp["user"]["username"] == test_user

    # 4. Authenticated Prediction
    print("4. Testing Authenticated Diagnosis (/predict)...")
    sample_path = Path("samples") / "tomato_late_blight.jpg"
    with open(sample_path, "rb") as f:
        file_bytes = f.read()
    
    upload_file = UploadFile(
        file=io.BytesIO(file_bytes),
        filename="tomato_late_blight.jpg",
        headers={"content-type": "image/jpeg"}
    )
    pred = await predict_disease(file=upload_file, authorization=f"Bearer {token}")
    print(f"   Prediction Result: {pred['disease']} ({pred['confidence_percentage']})")
    assert "Tomato Late Blight" in pred["disease"]

    # 5. History filtered by user
    print("5. Testing User-Specific History (/history)...")
    hist = get_history(limit=10, authorization=f"Bearer {token}")
    print(f"   User history count: {hist['total']}, User: {hist['user']}")
    assert hist["total"] >= 1
    assert hist["user"] == test_user
    assert hist["history"][0]["disease"] == pred["disease"]

    # 6. AI Agent Chat
    print("6. Testing AI Agent Chat (/chat)...")
    chat_resp = plant_health_chat(ChatRequest(
        message="What organic treatment can I spray immediately?",
        context={"disease": pred["disease"], "crop": pred["crop"], "severity": pred["severity"]}
    ))
    chat_answer = chat_resp["answer"] if isinstance(chat_resp, dict) else chat_resp.answer
    print(f"   Agent response preview: {chat_answer[:90]}...")
    assert len(chat_answer) > 20

    # 7. Logout
    print("7. Testing Logout Endpoint (/auth/logout)...")
    logout_resp = logout_user(authorization=f"Bearer {token}")
    print(f"   Logout response: {logout_resp['message']}")
    assert logout_resp["success"] is True

    print("\n==================================================")
    print("🎉 ALL END-TO-END WORKFLOW TESTS SUCCEEDED 100%!")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(test_complete_system())
