import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from auth_service import (
    get_auth_service,
    UserRegisterRequest,
    UserLoginRequest
)

print("--- Testing Auth Service ---")
auth_svc = get_auth_service()

# Test registration
test_email = "agronomist@plantvision.ai"
test_user = "demo_agronomist"

# Clear existing test user if present
for uid in list(auth_svc.users.keys()):
    if auth_svc.users[uid]["email"] == test_email or auth_svc.users[uid]["username"] == test_user:
        del auth_svc.users[uid]
auth_svc._save_users()

print("1. Testing User Registration...")
reg_req = UserRegisterRequest(
    username=test_user,
    email=test_email,
    password="SecurePassword2026!",
    full_name="Dr. Elena Green"
)
reg_res = auth_svc.register(reg_req)
token = reg_res["token"]
user_profile = reg_res["user"]
print(f"   Registered: {user_profile['full_name']} ({user_profile['email']})")
print(f"   Token generated: {token[:12]}...")
assert token is not None
assert user_profile["username"] == test_user

print("2. Testing Duplicate Registration Prevention...")
try:
    auth_svc.register(reg_req)
    assert False, "Should have failed on duplicate registration!"
except ValueError as e:
    print(f"   Successfully caught duplicate: {e}")

print("3. Testing User Login...")
login_req = UserLoginRequest(
    username_or_email=test_email,
    password="SecurePassword2026!"
)
login_res = auth_svc.login(login_req)
new_token = login_res["token"]
print(f"   Login successful! User: {login_res['user']['full_name']}")
assert new_token is not None

print("4. Testing Invalid Password Rejection...")
try:
    auth_svc.login(UserLoginRequest(username_or_email=test_email, password="WrongPassword!"))
    assert False, "Should have failed on invalid password!"
except ValueError as e:
    print(f"   Successfully caught invalid password: {e}")

print("5. Testing Token Validation (get_user_by_token)...")
profile = auth_svc.get_user_by_token(new_token)
assert profile is not None
assert profile["email"] == test_email
print(f"   Retrieved user profile: {profile['full_name']} (ID: {profile['id']})")

print("6. Testing User Logout...")
logout_success = auth_svc.logout(new_token)
assert logout_success is True
profile_after = auth_svc.get_user_by_token(new_token)
assert profile_after is None
print("   Session invalidated successfully on logout!")

print("7. Testing OTP Generation & Dispatch...")
from auth_service import SendOtpRequest, VerifyOtpRequest, UserResetPasswordRequest

# Send OTP via Email
send_email_res = auth_svc.send_otp(SendOtpRequest(identifier=test_email, channel="email"))
assert send_email_res["success"] is True
assert send_email_res["target_type"] == "email"
assert "otp" not in send_email_res  # Security: OTP must never leak in client response!
email_otp = auth_svc.otps[test_email]["otp"]
print(f"   Email OTP dispatched to {send_email_res['target']}: (Securely dispatched)")

# Send OTP via Mobile SMS (using user with phone)
phone_user_email = "farmer_otp@plantvision.ai"
phone_user_name = "farmer_otp"
for uid in list(auth_svc.users.keys()):
    if auth_svc.users[uid]["email"] == phone_user_email or auth_svc.users[uid]["username"] == phone_user_name:
        del auth_svc.users[uid]
auth_svc._save_users()

reg_phone_res = auth_svc.register(UserRegisterRequest(
    username=phone_user_name,
    email=phone_user_email,
    password="OldPassword123!",
    full_name="Farmer Joe",
    phone="+1 (555) 234-5678"
))
assert reg_phone_res["user"].get("id") is not None
print(f"   Registered user with phone: {reg_phone_res['user']['full_name']}")

send_sms_res = auth_svc.send_otp(SendOtpRequest(identifier=phone_user_email, channel="sms"))
assert send_sms_res["success"] is True
assert send_sms_res["target_type"] == "sms"
assert "otp" not in send_sms_res  # Security: OTP must never leak in client response!
sms_otp = auth_svc.otps[phone_user_email]["otp"]
print(f"   SMS OTP dispatched to {send_sms_res['target']}: (Securely dispatched)")

print("8. Testing OTP Verification...")
# Invalid OTP rejection
try:
    auth_svc.verify_otp(VerifyOtpRequest(identifier=test_email, otp="000000"))
    assert False, "Should have failed on invalid OTP!"
except ValueError as e:
    print(f"   Successfully caught invalid OTP: {e}")

# Valid OTP verification
verify_res = auth_svc.verify_otp(VerifyOtpRequest(identifier=test_email, otp=email_otp))
assert verify_res["success"] is True
print(f"   OTP verified successfully: {verify_res['message']}")

print("9. Testing Password Reset with OTP Enforcement...")
# Try reset with invalid user
try:
    auth_svc.reset_password(UserResetPasswordRequest(username_or_email="nonexistent@domain.com", new_password="NewSecretPassword123!", otp="123456"))
    assert False, "Should have failed for non-existent user!"
except ValueError as e:
    print(f"   Successfully caught invalid reset identifier: {e}")

# Try reset with wrong OTP for phone user
try:
    auth_svc.reset_password(UserResetPasswordRequest(username_or_email=phone_user_email, new_password="BrandNewPassword2026!", otp="999999"))
    assert False, "Should have failed on wrong OTP!"
except ValueError as e:
    print(f"   Successfully caught wrong OTP error: {e}")

# Try reset with too short password
try:
    auth_svc.reset_password(UserResetPasswordRequest(username_or_email=phone_user_email, new_password="123", otp=sms_otp))
    assert False, "Should have failed on short password!"
except ValueError as e:
    print(f"   Successfully caught short password error: {e}")

# Perform valid reset with verified OTP for test_email
reset_res = auth_svc.reset_password(UserResetPasswordRequest(username_or_email=test_email, new_password="BrandNewPassword2026!", otp=email_otp))
assert reset_res["success"] is True
print(f"   Password reset succeeded: {reset_res['message']}")

# Perform valid reset with OTP for phone user
reset_phone_res = auth_svc.reset_password(UserResetPasswordRequest(username_or_email=phone_user_email, new_password="NewFarmerPassword2026!", otp=sms_otp))
assert reset_phone_res["success"] is True
print(f"   Phone user password reset succeeded: {reset_phone_res['message']}")

# Verify old password fails
try:
    auth_svc.login(UserLoginRequest(username_or_email=test_email, password="SecurePassword2026!"))
    assert False, "Old password should not work anymore!"
except ValueError:
    print("   Old password rejected as expected.")

# Verify new password succeeds
login_with_new = auth_svc.login(UserLoginRequest(username_or_email=test_email, password="BrandNewPassword2026!"))
assert login_with_new["token"] is not None
print(f"   Logged in successfully with brand new password!")

# Restore default password for demo testing
restore_otp_res = auth_svc.send_otp(SendOtpRequest(identifier=test_email, channel="email"))
auth_svc.reset_password(UserResetPasswordRequest(username_or_email=test_email, new_password="SecurePassword2026!", otp=auth_svc.otps[test_email]["otp"]))

print("\n🎉 ALL AUTH SERVICE UNIT TESTS (INCLUDING 2-STEP OTP FORGOT PASSWORD) PASSED!")
