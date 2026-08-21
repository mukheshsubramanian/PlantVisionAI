import urllib.request
import urllib.parse
import json
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_URL = "http://127.0.0.1:8000"

def test_endpoints():
    print("--- 1. Testing GET / (Serving index.html with Home Page & Auth) ---")
    req = urllib.request.Request(f"{BASE_URL}/")
    with urllib.request.urlopen(req) as resp:
        content = resp.read().decode("utf-8")
        print(f"Status: {resp.status} | Content Length: {len(content)}")
        assert resp.status == 200
        assert "home-view" in content
        assert "auth-modal" in content
        assert "forgot-password-link" in content
        assert "reset-password-form" in content
        assert "Protect Every Leaf with" in content
        assert "How PlantVision AI Works" in content
        assert "profile-modal" in content
        print("   ✅ Home Page, Sign In/Up Modal, Forgot Password Form, and Profile Modal verified in HTML!")

    print("\n--- 2. Testing GET /static/style.css ---")
    with urllib.request.urlopen(f"{BASE_URL}/static/style.css") as resp:
        css = resp.read().decode("utf-8")
        assert resp.status == 200
        assert ".home-hero-container" in css
        assert ".auth-modal-card" in css
        assert ".auth-link-btn" in css
        assert ".toast-container" in css
        print(f"   ✅ Static CSS served successfully ({len(css)} bytes)!")

    print("\n--- 3. Testing GET /static/script.js ---")
    with urllib.request.urlopen(f"{BASE_URL}/static/script.js") as resp:
        js = resp.read().decode("utf-8")
        assert resp.status == 200
        assert "openAuthModal" in js
        assert "initAuthSession" in js
        assert "forgotPasswordLink" in js
        assert "resetPasswordForm" in js
        assert "showToast" in js
        print(f"   ✅ Static JavaScript served successfully ({len(js)} bytes)!")

    print("\n--- 4. Testing POST /auth/login (Demo Agronomist) ---")
    login_data = json.dumps({
        "username_or_email": "agronomist@plantvision.ai",
        "password": "SecurePassword2026!"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        token = data["token"]
        print(f"   ✅ Logged in user: {data['user']['full_name']} | Token: {token[:12]}...")
        assert token is not None

    print("\n--- 5. Testing GET /auth/me with Bearer Token ---")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        me_data = json.loads(resp.read().decode("utf-8"))
        print(f"   ✅ User profile retrieved: {me_data['user']['full_name']} ({me_data['user']['email']})")
        assert me_data["user"]["email"] == "agronomist@plantvision.ai"

    print("\n--- 6. Testing POST /auth/send-otp & POST /auth/reset-password with OTP ---")
    # Step 6a: Send OTP
    otp_data = json.dumps({
        "identifier": "farmer_john",
        "channel": "email"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/send-otp",
        data=otp_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        otp_res = json.loads(resp.read().decode("utf-8"))
        assert otp_res["success"] is True
        assert "otp" not in otp_res  # Security: OTP must never leak in client response!
        print(f"   ✅ OTP dispatched via HTTP API: {otp_res['message']}")

    from backend.auth_service import get_auth_service
    auth_svc = get_auth_service()
    auth_svc._load_data()
    gen_otp = auth_svc.otps["farmer_john"]["otp"]

    # Step 6b: Reset Password with OTP
    reset_data = json.dumps({
        "username_or_email": "farmer_john",
        "new_password": "JohnNewSecure2026!",
        "otp": gen_otp
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/reset-password",
        data=reset_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        reset_res = json.loads(resp.read().decode("utf-8"))
        assert reset_res["success"] is True
        print(f"   ✅ Password reset via HTTP API with OTP successful: {reset_res['message']}")

    # Restore farmer_john password
    otp_restore_req = urllib.request.Request(
        f"{BASE_URL}/auth/send-otp",
        data=json.dumps({"identifier": "farmer_john", "channel": "email"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(otp_restore_req) as resp:
        restore_otp_res = json.loads(resp.read().decode("utf-8"))
        assert restore_otp_res["success"] is True
        auth_svc._load_data()
        restore_otp = auth_svc.otps["farmer_john"]["otp"]

    restore_data = json.dumps({
        "username_or_email": "farmer_john",
        "new_password": "SecurePassword2026!",
        "otp": restore_otp
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/auth/reset-password",
        data=restore_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        pass

    print("\n--- 7. Testing GET /diseases ---")
    with urllib.request.urlopen(f"{BASE_URL}/diseases") as resp:
        cat = json.loads(resp.read().decode("utf-8"))
        diseases = cat.get("diseases", {})
        print(f"   ✅ Disease catalog returned {len(diseases)} disease profiles!")
        assert len(diseases) == 115

    print("\n--- 8. Testing POST /chat (AI Health Agent) ---")
    chat_payload = json.dumps({
        "message": "What is the organic treatment for tomato early blight?",
        "context": {"disease": "Tomato Early Blight", "crop": "Tomato", "severity": "Moderate"}
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat",
        data=chat_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        chat_data = json.loads(resp.read().decode("utf-8"))
        print(f"   ✅ AI Agent answered: {chat_data['answer'][:85]}...")
        print(f"   ✅ Suggested follow-ups: {chat_data['suggested_follow_ups']}")
        assert len(chat_data["answer"]) > 10

    print("\n--- 9. Testing GET /history with Bearer Token ---")
    req = urllib.request.Request(
        f"{BASE_URL}/history",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req) as resp:
        hist_data = json.loads(resp.read().decode("utf-8"))
        print(f"   ✅ User-linked scan history count: {hist_data['total']}")

    print("\n========================================================")
    print("🎉 ALL LIVE HTTP ENDPOINTS AND APP VIEWS VERIFIED 100%!")
    print("========================================================")

if __name__ == "__main__":
    test_endpoints()
