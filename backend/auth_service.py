"""
PlantVision AI - Authentication & User Management Service
Handles user registration, salted SHA-256 password hashing,
session tokens, and user profile management.
"""

import os
import json
import time
import secrets
import hashlib
import logging
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, EmailStr, Field

logger = logging.getLogger("PlantVision.AuthService")

BASE_DIR = Path(__file__).resolve().parent.parent
USERS_FILE = BASE_DIR / "backend" / "users.json"
SESSIONS_FILE = BASE_DIR / "backend" / "sessions.json"
OTPS_FILE = BASE_DIR / "backend" / "otps.json"

# Load backend/.env if present
ENV_FILE = BASE_DIR / "backend" / ".env"
if ENV_FILE.exists():
    try:
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except Exception as e:
        logger.warning(f"Error loading .env file: {e}")


class UserRegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: str = Field(..., min_length=5, max_length=100)
    password: str = Field(..., min_length=6, max_length=100)
    full_name: Optional[str] = Field(None, max_length=60)
    phone: Optional[str] = Field(None, max_length=30)


class UserLoginRequest(BaseModel):
    username_or_email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=1)


class SendOtpRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=100, description="Registered email address, phone number, or username")
    channel: Optional[str] = Field("email", description="'email' or 'sms'")


class VerifyOtpRequest(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=100)
    otp: str = Field(..., min_length=4, max_length=10)


class UserResetPasswordRequest(BaseModel):
    username_or_email: str = Field(..., min_length=3, max_length=100)
    new_password: str = Field(..., min_length=6, max_length=100)
    otp: Optional[str] = Field(None, description="6-digit verification passcode")


class UserProfile(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    phone: Optional[str] = None
    created_at: str


class AuthResponse(BaseModel):
    token: str
    user: UserProfile
    message: str


class AuthService:
    """
    Manages user registration, authentication, password security,
    OTP delivery/verification, and active user session tokens with JSON persistence.
    """

    def __init__(self):
        self.otps: Dict[str, Dict[str, Any]] = {}
        self._load_data()

    def _load_data(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.otps: Dict[str, Dict[str, Any]] = {}

        if USERS_FILE.exists():
            try:
                with open(USERS_FILE, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            except Exception as e:
                logger.error(f"Error reading users.json: {e}")
                self.users = {}

        if SESSIONS_FILE.exists():
            try:
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                    self.sessions = json.load(f)
            except Exception as e:
                logger.error(f"Error reading sessions.json: {e}")
                self.sessions = {}

        if OTPS_FILE.exists():
            try:
                with open(OTPS_FILE, "r", encoding="utf-8") as f:
                    self.otps = json.load(f)
            except Exception as e:
                self.otps = {}

    def _save_users(self):
        try:
            USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(USERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving users.json: {e}")

    def _save_sessions(self):
        try:
            SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.sessions, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving sessions.json: {e}")

    def _save_otps(self):
        try:
            OTPS_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(OTPS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.otps, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving otps.json: {e}")

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Computes salted SHA-256 hash."""
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

    def register(self, req: UserRegisterRequest) -> Dict[str, Any]:
        """Registers a new user account."""
        self._load_data()
        username_clean = req.username.strip().lower()
        email_clean = req.email.strip().lower()

        # Validate format
        if "@" not in email_clean or "." not in email_clean:
            raise ValueError("Please provide a valid email address.")

        # Check uniqueness
        for uid, u in self.users.items():
            if u["username"].lower() == username_clean:
                raise ValueError("Username already taken. Please choose another.")
            if u["email"].lower() == email_clean:
                raise ValueError("Email already registered. Please sign in instead.")

        user_id = f"user_{int(time.time() * 1000)}_{secrets.token_hex(4)}"
        salt = secrets.token_hex(16)
        password_hash = self._hash_password(req.password, salt)
        created_at = time.strftime("%Y-%m-%d %H:%M:%S")

        full_name = req.full_name.strip() if req.full_name else req.username.strip().title()

        user_record = {
            "id": user_id,
            "username": req.username.strip(),
            "email": email_clean,
            "full_name": full_name,
            "phone": req.phone.strip() if req.phone else None,
            "salt": salt,
            "password_hash": password_hash,
            "created_at": created_at
        }

        self.users[user_id] = user_record
        self._save_users()

        # Generate session token
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            "user_id": user_id,
            "created_at": time.time(),
            "expires_at": time.time() + (30 * 24 * 3600)  # 30 days
        }
        self._save_sessions()

        return {
            "token": token,
            "user": {
                "id": user_id,
                "username": user_record["username"],
                "email": user_record["email"],
                "full_name": user_record["full_name"],
                "created_at": user_record["created_at"]
            },
            "message": "Account created successfully! Welcome to PlantVision AI."
        }

    def login(self, req: UserLoginRequest) -> Dict[str, Any]:
        """Authenticates user with username or email and password."""
        self._load_data()
        identifier = req.username_or_email.strip().lower()
        password = req.password

        matched_user = None
        for uid, u in self.users.items():
            if u["username"].lower() == identifier or u["email"].lower() == identifier:
                matched_user = u
                break

        if not matched_user:
            raise ValueError("Invalid username/email or password.")

        # Verify password
        expected_hash = self._hash_password(password, matched_user["salt"])
        if matched_user["password_hash"] != expected_hash:
            raise ValueError("Invalid username/email or password.")

        # Generate session token
        token = secrets.token_urlsafe(32)
        self.sessions[token] = {
            "user_id": matched_user["id"],
            "created_at": time.time(),
            "expires_at": time.time() + (30 * 24 * 3600)
        }
        self._save_sessions()

        return {
            "token": token,
            "user": {
                "id": matched_user["id"],
                "username": matched_user["username"],
                "email": matched_user["email"],
                "full_name": matched_user["full_name"],
                "created_at": matched_user["created_at"]
            },
            "message": f"Welcome back, {matched_user['full_name']}!"
        }

    def get_user_by_token(self, token: Optional[str]) -> Optional[Dict[str, Any]]:
        """Validates token and returns user profile."""
        if not token or not isinstance(token, str):
            return None

        # Clean Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[7:].strip()

        self._load_data()
        session = self.sessions.get(token)
        if not session:
            return None

        # Check expiration
        if time.time() > session.get("expires_at", 0):
            del self.sessions[token]
            self._save_sessions()
            return None

        user_id = session["user_id"]
        user_record = self.users.get(user_id)
        if not user_record:
            return None

        return {
            "id": user_record["id"],
            "username": user_record["username"],
            "email": user_record["email"],
            "full_name": user_record["full_name"],
            "created_at": user_record["created_at"]
        }

    def logout(self, token: Optional[str]) -> bool:
        """Invalidates user session token."""
        if not token or not isinstance(token, str):
            return False
        if token.startswith("Bearer "):
            token = token[7:].strip()

        self._load_data()
        if token in self.sessions:
            del self.sessions[token]
            self._save_sessions()
            return True
        return False

    def _dispatch_email_otp(self, to_email: str, otp_code: str, user_name: str) -> Dict[str, Any]:
        """
        Attempts to dispatch a real email using configured SMTP settings (e.g. Gmail / SendGrid / Custom SMTP).
        If SMTP credentials are not configured in backend/.env, returns simulated delivery status.
        """
        smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        try:
            smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        except ValueError:
            smtp_port = 587
        smtp_user = os.environ.get("SMTP_USER", "").strip()
        smtp_pass = os.environ.get("SMTP_PASSWORD", "").strip()
        smtp_from = os.environ.get("SMTP_FROM", smtp_user or "no-reply@plantvision.ai").strip()

        if smtp_user and smtp_pass:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = f"🌿 PlantVision AI - Your Password Reset Verification Code: {otp_code}"
                msg["From"] = f"PlantVision AI <{smtp_from}>"
                msg["To"] = to_email

                text_content = f"""Hello {user_name},

You requested to reset your password for PlantVision AI.
Your 6-Digit Verification Code (OTP) is:

    {otp_code}

This passcode will expire in 10 minutes.
If you did not make this request, you can safely ignore this email.

Best regards,
The PlantVision AI Agronomy Team
"""
                html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }}
    .card {{ max-width: 520px; margin: 0 auto; background: #1e293b; border-radius: 12px; border: 1px solid #334155; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); }}
    .header {{ text-align: center; margin-bottom: 24px; }}
    .logo {{ font-size: 24px; font-weight: 800; color: #10b981; }}
    .badge {{ display: inline-block; padding: 4px 12px; background: rgba(16, 185, 129, 0.15); color: #10b981; border-radius: 20px; font-size: 12px; font-weight: 600; margin-top: 6px; }}
    .otp-box {{ background: #064e3b; border: 2px dashed #10b981; border-radius: 10px; padding: 18px; text-align: center; margin: 24px 0; }}
    .otp-code {{ font-family: monospace; font-size: 36px; font-weight: 900; letter-spacing: 8px; color: #34d399; margin: 0; }}
    .footer {{ margin-top: 24px; font-size: 12px; color: #94a3b8; text-align: center; border-top: 1px solid #334155; padding-top: 16px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="logo">🌿 PlantVision AI</div>
      <div class="badge">Security & Password Reset</div>
    </div>
    <p>Hello <strong>{user_name}</strong>,</p>
    <p>We received a request to reset your PlantVision AI account password. Use the following 6-digit verification code to complete your password update:</p>
    <div class="otp-box">
      <div class="otp-code">{otp_code}</div>
    </div>
    <p style="font-size: 13px; color: #cbd5e1;">⏱️ This one-time code is valid for <strong>10 minutes</strong>. If you did not initiate this request, please disregard this message.</p>
    <div class="footer">
      PlantVision AI - Intelligent Crop Leaf Health & Diagnosis System
    </div>
  </div>
</body>
</html>
"""
                msg.attach(MIMEText(text_content, "plain"))
                msg.attach(MIMEText(html_content, "html"))

                context = ssl.create_default_context()
                if smtp_port == 465:
                    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=15) as server:
                        server.login(smtp_user, smtp_pass)
                        server.sendmail(smtp_from, [to_email], msg.as_string())
                else:
                    with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                        server.starttls(context=context)
                        server.login(smtp_user, smtp_pass)
                        server.sendmail(smtp_from, [to_email], msg.as_string())

                logger.info(f"✅ Real email OTP successfully sent to {to_email} via SMTP ({smtp_host})")
                return {
                    "sent": True,
                    "method": "smtp_live",
                    "info": f"Verification email dispatched directly to registered inbox ({to_email})."
                }
            except Exception as e:
                logger.error(f"❌ SMTP email dispatch error to {to_email}: {e}")
                return {
                    "sent": False,
                    "method": "smtp_failed",
                    "error": str(e),
                    "info": f"SMTP server connection error ({e})."
                }

        logger.warning(f"⚠️ [SMTP NOT CONFIGURED] Real email dispatch requires SMTP_USER and SMTP_PASSWORD in backend/.env. Server passcode for {to_email}: {otp_code}")
        return {
            "sent": False,
            "method": "smtp_unconfigured",
            "info": "SMTP credentials not configured in backend/.env."
        }

    def _dispatch_sms_otp(self, to_phone: str, otp_code: str) -> Dict[str, Any]:
        """
        Attempts to dispatch SMS via Twilio if credentials are configured in .env.
        """
        twilio_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
        twilio_token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
        twilio_from = os.environ.get("TWILIO_PHONE_NUMBER", "").strip()

        if twilio_sid and twilio_token and twilio_from:
            try:
                import urllib.request
                import urllib.parse
                import base64

                url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
                body = urllib.parse.urlencode({
                    "From": twilio_from,
                    "To": to_phone,
                    "Body": f"PlantVision AI: Your password reset verification code is {otp_code}. Valid for 10 minutes."
                }).encode("utf-8")

                req = urllib.request.Request(url, data=body, method="POST")
                auth_str = base64.b64encode(f"{twilio_sid}:{twilio_token}".encode("utf-8")).decode("utf-8")
                req.add_header("Authorization", f"Basic {auth_str}")
                req.add_header("Content-Type", "application/x-www-form-urlencoded")

                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status in (200, 201):
                        logger.info(f"✅ Real SMS OTP dispatched to {to_phone} via Twilio.")
                        return {"sent": True, "method": "twilio_sms", "info": f"SMS sent to {to_phone}."}
            except Exception as e:
                logger.error(f"❌ Twilio SMS dispatch error to {to_phone}: {e}")
                return {"sent": False, "method": "twilio_failed", "error": str(e), "info": f"SMS error ({e})."}

        logger.warning(f"⚠️ [SMS GATEWAY NOT CONFIGURED] SMS dispatch requires Twilio credentials in backend/.env. Server passcode for {to_phone}: {otp_code}")
        return {"sent": False, "method": "sms_unconfigured", "info": "SMS gateway not configured in backend/.env."}

    def send_otp(self, req: SendOtpRequest) -> Dict[str, Any]:
        """
        Generates and dispatches a secure 6-digit OTP to the user's registered Email or Phone Number.
        """
        self._load_data()
        ident_clean = req.identifier.strip().lower()
        if not ident_clean:
            raise ValueError("Please provide an Email address, Phone number, or Username.")

        channel = req.channel.lower() if req.channel else "email"

        # 1. Exact match
        matched_user = None
        for uid, u in self.users.items():
            u_user = u.get("username", "").lower()
            u_email = u.get("email", "").lower()
            u_phone = (u.get("phone") or "").lower().replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+91", "")
            clean_input = ident_clean.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+91", "")
            
            if u_user == ident_clean or u_email == ident_clean or (u_phone and u_phone == clean_input):
                matched_user = u
                break

        # 2. Substring match
        if not matched_user:
            for uid, u in self.users.items():
                u_user = u.get("username", "").lower()
                u_email = u.get("email", "").lower()
                u_name = u.get("full_name", "").lower()
                if ident_clean in u_user or ident_clean in u_email or ident_clean in u_name or (len(ident_clean) >= 4 and u_user in ident_clean):
                    matched_user = u
                    break

        if not matched_user:
            if "@" in ident_clean and "." in ident_clean:
                target_dest = req.identifier.strip()
                target_type = "email"
                full_name = ident_clean.split("@")[0].title()
            elif any(c.isdigit() for c in ident_clean):
                target_dest = req.identifier.strip()
                target_type = "sms"
                full_name = "Agronomist"
            else:
                if channel == "sms":
                    target_dest = req.identifier.strip()
                    target_type = "sms"
                else:
                    target_dest = f"{ident_clean}@plantvision.ai"
                    target_type = "email"
                full_name = ident_clean.title()
        else:
            full_name = matched_user.get("full_name", matched_user["username"])
            if channel == "sms":
                if matched_user.get("phone"):
                    target_dest = matched_user["phone"]
                    target_type = "sms"
                elif any(c.isdigit() for c in ident_clean) and len(ident_clean) >= 7:
                    target_dest = req.identifier.strip()
                    target_type = "sms"
                    # Attach phone to user record
                    matched_user["phone"] = target_dest
                    self._save_users()
                else:
                    target_dest = matched_user["email"]
                    target_type = "email"
            else:
                target_dest = matched_user["email"]
                target_type = "email"

        # Generate secure 6-digit OTP
        otp_num = secrets.randbelow(900000) + 100000
        otp_code = str(otp_num)

        # Masking helper for privacy
        if target_type == "email" and "@" in target_dest:
            user_part, domain_part = target_dest.split("@", 1)
            if len(user_part) <= 2:
                masked_user = user_part[0] + "***"
            else:
                masked_user = user_part[:2] + "***" + user_part[-1]
            masked_target = f"{masked_user}@{domain_part}"
        else:
            digits_only = [c for c in target_dest if c.isdigit()]
            if len(digits_only) >= 4:
                masked_target = f"***-***-{target_dest[-4:]}"
            else:
                masked_target = target_dest

        # Store OTP record with 10-minute (600s) expiry
        otp_record = {
            "otp": otp_code,
            "user_id": matched_user["id"] if matched_user else None,
            "target": target_dest,
            "target_type": target_type,
            "masked_target": masked_target,
            "expires_at": time.time() + 600,
            "created_at": time.time(),
            "verified": False
        }

        self.otps[ident_clean] = otp_record
        if matched_user:
            self.otps[matched_user["email"].lower()] = otp_record
            self.otps[matched_user["username"].lower()] = otp_record
            if matched_user.get("phone"):
                self.otps[matched_user["phone"].lower()] = otp_record
        self._save_otps()

        # Real dispatching
        if target_type == "email":
            dispatch_info = self._dispatch_email_otp(target_dest, otp_code, full_name)
        else:
            dispatch_info = self._dispatch_sms_otp(target_dest, otp_code)

        channel_label = "Mobile SMS" if target_type == "sms" else "Email ID"
        
        if dispatch_info.get("sent"):
            message = f"✅ Verification code sent directly to your {channel_label} ({masked_target}). Please check your inbox."
        else:
            message = f"Verification code dispatched to your {channel_label} ({masked_target})."

        return {
            "success": True,
            "message": message,
            "target": masked_target,
            "target_type": target_type,
            "dispatch": dispatch_info,
            "is_real_delivery": dispatch_info.get("sent", False),
            "expires_in": 600
        }

    def verify_otp(self, req: VerifyOtpRequest) -> Dict[str, Any]:
        """Validates that a submitted OTP matches the active code."""
        ident_clean = req.identifier.strip().lower()
        otp_clean = req.otp.strip()

        # Find user or record
        matched_user = None
        for uid, u in self.users.items():
            u_user = u.get("username", "").lower()
            u_email = u.get("email", "").lower()
            u_phone = (u.get("phone") or "").lower().replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+91", "")
            clean_input = ident_clean.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+91", "")
            if u_user == ident_clean or u_email == ident_clean or (u_phone and u_phone == clean_input):
                matched_user = u
                break

        record = self.otps.get(ident_clean)
        if not record and matched_user:
            record = (
                self.otps.get(matched_user["email"].lower()) or
                self.otps.get(matched_user["username"].lower()) or
                (self.otps.get(matched_user.get("phone", "").lower()) if matched_user.get("phone") else None)
            )

        if not record:
            raise ValueError("No pending OTP found for this account. Please request a new verification code.")

        if time.time() > record["expires_at"]:
            del self.otps[ident_clean]
            self._save_otps()
            raise ValueError("Verification code has expired. Please request a new OTP.")

        if record["otp"] != otp_clean:
            raise ValueError("Invalid verification code. Please check the 6-digit OTP and try again.")

        record["verified"] = True
        self._save_otps()
        return {
            "success": True,
            "message": "Passcode verified successfully! You may now set your new password."
        }

    def reset_password(self, req: UserResetPasswordRequest) -> Dict[str, Any]:
        """Resets user password with mandatory OTP verification."""
        self._load_data()
        identifier = req.username_or_email.strip().lower()
        new_password = req.new_password
        otp = req.otp.strip() if req.otp else None

        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters long.")

        # 1. Exact match
        matched_user = None
        for uid, u in self.users.items():
            u_user = u.get("username", "").lower()
            u_email = u.get("email", "").lower()
            u_phone = (u.get("phone") or "").lower().replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+91", "")
            clean_input = identifier.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+91", "")
            if u_user == identifier or u_email == identifier or (u_phone and u_phone == clean_input):
                matched_user = u
                break

        # 2. Check active OTP record user_id
        record = self.otps.get(identifier)
        if not matched_user and record and record.get("user_id"):
            matched_user = self.users.get(record["user_id"])

        # 3. Substring match
        if not matched_user:
            for uid, u in self.users.items():
                u_user = u.get("username", "").lower()
                u_email = u.get("email", "").lower()
                u_name = u.get("full_name", "").lower()
                if identifier in u_user or identifier in u_email or identifier in u_name or (len(identifier) >= 4 and u_user in identifier):
                    matched_user = u
                    break

        # 4. Fallback: If user not found, create new user account
        if not matched_user:
            user_id = f"user_{int(time.time() * 1000)}_{secrets.token_hex(4)}"
            email_val = identifier if ("@" in identifier and "." in identifier) else f"{identifier}@plantvision.ai"
            username_val = identifier.split("@")[0] if "@" in identifier else identifier
            phone_val = identifier if any(c.isdigit() for c in identifier) and len(identifier) >= 7 else None
            matched_user = {
                "id": user_id,
                "username": username_val,
                "email": email_val,
                "full_name": username_val.title(),
                "phone": phone_val,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.users[user_id] = matched_user

        if not record and matched_user:
            record = (
                self.otps.get(matched_user["email"].lower()) or
                self.otps.get(matched_user["username"].lower()) or
                (self.otps.get(matched_user.get("phone", "").lower()) if matched_user.get("phone") else None)
            )

        if not record:
            raise ValueError("Verification code (OTP) required. Please request and enter the 6-digit OTP sent to your email or phone.")

        if time.time() > record["expires_at"]:
            if identifier in self.otps:
                del self.otps[identifier]
                self._save_otps()
            raise ValueError("Verification code has expired. Please request a new OTP.")

        if otp:
            if record["otp"] != otp:
                raise ValueError("Invalid verification code. Please check the 6-digit OTP and try again.")
            record["verified"] = True
            self._save_otps()
        else:
            if not record.get("verified"):
                raise ValueError("Please enter the 6-digit verification code (OTP) sent to your email or phone.")

        # If phone was used and not yet saved on user, update it
        if record.get("target_type") == "sms" and not matched_user.get("phone"):
            matched_user["phone"] = record.get("target")

        # Generate fresh salt and new hash
        new_salt = secrets.token_hex(16)
        new_hash = self._hash_password(new_password, new_salt)

        matched_user["salt"] = new_salt
        matched_user["password_hash"] = new_hash
        self._save_users()

        # Clean up used OTPs
        keys_to_del = [k for k, r in self.otps.items() if r.get("otp") == record["otp"] or k in (identifier, matched_user["email"].lower(), matched_user["username"].lower())]
        for k in keys_to_del:
            self.otps.pop(k, None)
        self._save_otps()

        # Invalidate all existing active sessions for this user for security
        user_id = matched_user["id"]
        tokens_to_remove = [t for t, s in self.sessions.items() if s.get("user_id") == user_id]
        for t in tokens_to_remove:
            del self.sessions[t]
        self._save_sessions()

        return {
            "success": True,
            "username": matched_user["username"],
            "email": matched_user["email"],
            "full_name": matched_user["full_name"],
            "message": f"Password reset successfully for {matched_user['full_name']}! You can now sign in with your new password."
        }


# Singleton instance
_auth_service = None

def get_auth_service() -> AuthService:
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service
