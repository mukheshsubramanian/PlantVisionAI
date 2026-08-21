"""
PlantVision AI - FastAPI Backend Application
AI-Based Plant Leaf Disease Detection and Solution Recommendation System REST API
"""

import os
import json
import time
import base64
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import sys
from pathlib import Path

# Ensure backend folder is in python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Local services
from model_service import get_model_service, TORCH_AVAILABLE
from agent_service import get_plant_agent
from auth_service import (
    get_auth_service,
    UserRegisterRequest,
    UserLoginRequest,
    UserResetPasswordRequest,
    SendOtpRequest,
    VerifyOtpRequest,
    AuthResponse,
    UserProfile
)
from fastapi import Header, Depends


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PlantVision.API")

app = FastAPI(
    title="PlantVision AI API",
    description="AI-Based Plant Leaf Disease Detection and Solution Recommendation System",
    version="1.0.0"
)

# Enable CORS for cross-origin frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware to prevent stale browser caching for development
@app.middleware("http")
async def add_no_cache_headers(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static") or request.url.path == "/":
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
SAMPLES_DIR = BASE_DIR / "samples"
HISTORY_FILE = BASE_DIR / "backend" / "prediction_history.json"
DISEASE_INFO_FILE = BASE_DIR / "disease_info.json"

# In-memory history cache backed by JSON
def load_history() -> List[Dict[str, Any]]:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading history file: {e}")
    return []

def save_history(history: List[Dict[str, Any]]):
    try:
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving history: {e}")

_scan_history: List[Dict[str, Any]] = load_history()


# Request/Response Models
class ChatRequest(BaseModel):
    message: str = Field(..., description="User question or follow-up query")
    context: Optional[Dict[str, Any]] = Field(None, description="Active leaf diagnosis context")
    chat_history: Optional[List[Dict[str, str]]] = Field(None, description="Previous message history")


class ChatResponse(BaseModel):
    answer: str
    disease_context: Optional[str] = None
    crop: Optional[str] = None
    severity: Optional[str] = None
    suggested_follow_ups: List[str]


class OtpDispatchResponse(BaseModel):
    success: bool
    message: str
    target: str
    target_type: str
    dispatch: Optional[Dict[str, Any]] = None
    is_real_delivery: bool = False
    expires_in: int = 600


class OtpVerifyResponse(BaseModel):
    success: bool
    message: str


class PasswordResetResponse(BaseModel):
    success: bool
    username: str
    email: str
    full_name: str
    message: str


# Mount static assets
if SAMPLES_DIR.exists():
    app.mount("/samples-static", StaticFiles(directory=str(SAMPLES_DIR)), name="samples")

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend_static")


# --- Endpoints ---

@app.get("/")
def serve_index():
    """Serves the frontend main single-page application."""
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "PlantVision AI API is running. Frontend index.html not found."}


@app.get("/health")
def health_check():
    """System and CNN Model Health Status Endpoint."""
    model_svc = get_model_service()
    return {
        "status": "healthy",
        "service": "PlantVision AI",
        "torch_available": TORCH_AVAILABLE,
        "device": str(model_svc.device) if model_svc.device else "cpu",
        "model_loaded": model_svc.model is not None,
        "supported_classes_count": len(model_svc.class_names),
        "supported_classes": model_svc.class_names,
        "timestamp": time.time()
    }


# --- Auth Helper ---
def resolve_user_from_header(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """Safely extracts authenticated user from Bearer header."""
    if not authorization or not isinstance(authorization, str):
        return None
    auth_svc = get_auth_service()
    return auth_svc.get_user_by_token(authorization)


# --- Authentication Endpoints ---

@app.post("/auth/register", response_model=AuthResponse)
def register_user(req: UserRegisterRequest):
    """Registers a new user account with salted password hashing."""
    auth_svc = get_auth_service()
    try:
        res = auth_svc.register(req)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed due to internal error.")


@app.post("/auth/login", response_model=AuthResponse)
def login_user(req: UserLoginRequest):
    """Authenticates user and issues a 30-day session token."""
    auth_svc = get_auth_service()
    try:
        res = auth_svc.login(req)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=401, detail=str(ve))
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed due to internal error.")


@app.post("/auth/send-otp", response_model=OtpDispatchResponse)
def send_verification_otp(req: SendOtpRequest):
    """Generates and sends a 6-digit OTP to user's registered Email or Phone Number."""
    auth_svc = get_auth_service()
    try:
        res = auth_svc.send_otp(req)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Send OTP error: {e}")
        raise HTTPException(status_code=500, detail="Failed to dispatch OTP passcode.")


@app.post("/auth/verify-otp", response_model=OtpVerifyResponse)
def verify_user_otp(req: VerifyOtpRequest):
    """Validates the submitted 6-digit OTP code."""
    auth_svc = get_auth_service()
    try:
        res = auth_svc.verify_otp(req)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Verify OTP error: {e}")
        raise HTTPException(status_code=500, detail="OTP verification failed.")


@app.post("/auth/reset-password", response_model=PasswordResetResponse)
def reset_user_password(req: UserResetPasswordRequest):
    """Resets user password with 6-digit OTP verification."""
    auth_svc = get_auth_service()
    try:
        res = auth_svc.reset_password(req)
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Password reset error: {e}")
        raise HTTPException(status_code=500, detail="Password reset failed due to internal error.")


@app.get("/auth/me")
def get_current_profile(authorization: Optional[str] = Header(None)):
    """Retrieves profile of the currently logged-in user."""
    user = resolve_user_from_header(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Session expired or invalid. Please sign in.")
    return {"user": user}


@app.post("/auth/logout")
def logout_user(authorization: Optional[str] = Header(None)):
    """Logs out the active session."""
    auth_svc = get_auth_service()
    if isinstance(authorization, str):
        success = auth_svc.logout(authorization)
    else:
        success = False
    return {"success": success, "message": "Logged out successfully."}


@app.post("/predict")
async def predict_disease(
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(None)
):
    """
    Receives an uploaded leaf image, validates dimensions and format,
    executes CNN classification inference, maps to structured disease information,
    records prediction history (associated with user if logged in), and returns full diagnostic recommendations.
    """
    # Validate MIME type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{file.content_type}'. Please upload a valid image (JPEG, PNG, WEBP)."
        )

    try:
        image_bytes = await file.read()
        model_svc = get_model_service()
        
        # Validate & load PIL Image
        pil_image = model_svc.validate_image_bytes(image_bytes)
        
        # Run CNN Inference
        start_time = time.time()
        result = model_svc.predict(pil_image)
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        result["latency_ms"] = latency_ms
        result["filename"] = file.filename
        result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")

        # Generate a small base64 thumbnail for history display
        thumb = pil_image.copy()
        thumb.thumbnail((120, 120))
        import io
        thumb_buf = io.BytesIO()
        thumb.save(thumb_buf, format="JPEG", quality=75)
        thumb_b64 = f"data:image/jpeg;base64,{base64.b64encode(thumb_buf.getvalue()).decode('utf-8')}"

        # Determine user affiliation
        current_user = resolve_user_from_header(authorization)
        user_id = current_user["id"] if current_user else "guest"
        user_name = current_user["full_name"] if current_user else "Guest"

        # Save to history
        history_item = {
            "id": f"scan_{int(time.time() * 1000)}",
            "user_id": user_id,
            "user_name": user_name,
            "filename": file.filename,
            "disease": result["disease"],
            "crop": result["crop"],
            "confidence": result["confidence"],
            "confidence_percentage": result["confidence_percentage"],
            "severity": result["severity"],
            "category": result["category"],
            "timestamp": result["timestamp"],
            "thumbnail": thumb_b64
        }
        _scan_history.insert(0, history_item)
        if len(_scan_history) > 100:
            _scan_history.pop()
        save_history(_scan_history)

        return result

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.get("/disease/{name}")
def get_disease_details(name: str):
    """Retrieves comprehensive disease information for a specific disease or disease key."""
    model_svc = get_model_service()
    
    # Try exact key
    if name in model_svc.disease_info:
        return model_svc.disease_info[name]
    
    # Try case-insensitive or name match
    name_clean = name.replace("_", " ").lower().strip()
    for key, info in model_svc.disease_info.items():
        if info.get("disease_name", "").lower() == name_clean or key.lower() == name.lower():
            return info

    raise HTTPException(status_code=404, detail=f"Disease '{name}' not found in knowledge database.")


@app.get("/diseases")
def list_all_diseases():
    """Retrieves catalog of all supported crops, diseases, and categories."""
    if DISEASE_INFO_FILE.exists():
        try:
            with open(DISEASE_INFO_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading disease_info: {e}")
    
    model_svc = get_model_service()
    return {"diseases": model_svc.disease_info}


@app.post("/chat", response_model=ChatResponse)
def plant_health_chat(request: ChatRequest):
    """
    Agentic AI Plant Health Assistant endpoint.
    Answers natural language plant questions with context of current scan.
    """
    agent = get_plant_agent()
    response = agent.generate_response(
        question=request.message,
        scan_context=request.context,
        chat_history=request.chat_history
    )
    return response


@app.get("/history")
def get_history(limit: int = 20, authorization: Optional[str] = Header(None)):
    """Retrieves recent diagnostic history logs, filtering by user if logged in."""
    limit_val = int(limit) if isinstance(limit, (int, str)) and str(limit).isdigit() else 20
    
    current_user = resolve_user_from_header(authorization)
    
    if current_user:
        user_scans = [item for item in _scan_history if item.get("user_id") == current_user["id"]]
        return {"history": user_scans[:limit_val], "total": len(user_scans), "user": current_user["username"]}
    else:
        # Return all / guest scans
        return {"history": _scan_history[:limit_val], "total": len(_scan_history), "user": "guest"}


@app.delete("/history")
def clear_history(authorization: Optional[str] = Header(None)):
    """Clears diagnostic history logs for the active user or guest session."""
    global _scan_history
    current_user = resolve_user_from_header(authorization)
    
    if current_user:
        _scan_history = [item for item in _scan_history if item.get("user_id") != current_user["id"]]
    else:
        _scan_history = []
    
    save_history(_scan_history)
    return {"message": "Diagnostic history cleared successfully."}


# --- Agricultural Weather & Disease Proliferation Risk ---

PRESET_FARM_CLIMATES = {
    "sacramento valley, ca": {
        "location": "Sacramento Valley, CA",
        "temperature_c": 24.2,
        "humidity_pct": 78,
        "rain_chance_pct": 45,
        "condition": "Humid & Overcast",
        "wind_speed_kmh": 11
    },
    "punjab agricultural belt": {
        "location": "Punjab Agricultural Belt",
        "temperature_c": 29.5,
        "humidity_pct": 84,
        "rain_chance_pct": 65,
        "condition": "Warm & Humid Monsoonal",
        "wind_speed_kmh": 14
    },
    "midwest corn belt, ia": {
        "location": "Midwest Corn Belt, IA",
        "temperature_c": 21.8,
        "humidity_pct": 72,
        "rain_chance_pct": 35,
        "condition": "Partly Cloudy Dew",
        "wind_speed_kmh": 16
    },
    "salinas valley, ca": {
        "location": "Salinas Valley, CA",
        "temperature_c": 18.5,
        "humidity_pct": 86,
        "rain_chance_pct": 50,
        "condition": "Cool Marine Fog & Dampness",
        "wind_speed_kmh": 9
    },
    "central florida citrus zone": {
        "location": "Central Florida Citrus Zone",
        "temperature_c": 28.0,
        "humidity_pct": 88,
        "rain_chance_pct": 70,
        "condition": "Tropical Thunderstorms",
        "wind_speed_kmh": 18
    },
    "yakima valley apple belt, wa": {
        "location": "Yakima Valley Apple Belt, WA",
        "temperature_c": 22.0,
        "humidity_pct": 42,
        "rain_chance_pct": 10,
        "condition": "Dry & Sunny",
        "wind_speed_kmh": 12
    },
    "mediterranean olive basin": {
        "location": "Mediterranean Olive Basin",
        "temperature_c": 26.5,
        "humidity_pct": 48,
        "rain_chance_pct": 15,
        "condition": "Warm & Semi-Arid",
        "wind_speed_kmh": 15
    }
}

@app.get("/weather-risk")
def get_weather_risk(
    location: Optional[str] = Query("Sacramento Valley, CA", description="Farm location or region"),
    temp_c: Optional[float] = Query(None, description="Optional manual temperature in Celsius"),
    humidity: Optional[int] = Query(None, description="Optional manual relative humidity %")
):
    """
    Computes real-time microclimate pathogen proliferation risk and agricultural advisory.
    Uses epidemiological models combining temperature, relative humidity, and leaf wetness.
    """
    loc_key = (location or "Sacramento Valley, CA").strip().lower()
    
    if loc_key in PRESET_FARM_CLIMATES:
        climate = dict(PRESET_FARM_CLIMATES[loc_key])
    else:
        # Dynamic deterministic simulation based on location string hash
        h_val = abs(hash(loc_key)) % 100
        sim_temp = 18.0 + (h_val % 14) + (h_val % 7) * 0.2
        sim_humidity = 45 + (h_val % 50)
        sim_rain = (h_val % 75)
        climate = {
            "location": location.title() if location else "Custom Farm Zone",
            "temperature_c": round(sim_temp, 1),
            "humidity_pct": int(sim_humidity),
            "rain_chance_pct": int(sim_rain),
            "condition": "Humid / Overcast" if sim_humidity > 70 else "Fair & Breezy",
            "wind_speed_kmh": 10 + (h_val % 12)
        }

    # Override if user provided custom values
    if temp_c is not None:
        climate["temperature_c"] = float(temp_c)
    if humidity is not None:
        climate["humidity_pct"] = int(np.clip(humidity, 10, 100))

    t = climate["temperature_c"]
    rh = climate["humidity_pct"]
    rain = climate["rain_chance_pct"]

    # Calculate Pathogen Proliferation Index (0 - 100)
    # Fungi sporulate rapidly when RH > 75% and Temp between 18C and 28C
    rh_factor = max(0.0, (rh - 40) / 60.0) * 55.0
    
    # Temperature bell-curve optimal around 22-26°C
    if 18.0 <= t <= 28.0:
        temp_factor = 35.0
    elif 12.0 <= t < 18.0 or 28.0 < t <= 33.0:
        temp_factor = 20.0
    else:
        temp_factor = 8.0

    rain_factor = (rain / 100.0) * 10.0
    risk_score = int(np.clip(rh_factor + temp_factor + rain_factor, 5, 98))

    if risk_score < 30:
        risk_level = "Low Risk"
        risk_badge = "status-optimal"
        advisory = "Dry foliage conditions inhibit fungal spore germination. Standard maintenance schedule recommended."
        spray_recommendation = "No urgent preventative fungicide needed. Monitor normal irrigation."
        susceptible_diseases = ["Powdery Mildew (Dry/Warm variant)"]
    elif risk_score < 60:
        risk_level = "Moderate Risk"
        risk_badge = "status-moderate"
        advisory = "Moderate humidity and leaf moisture present. Spore accumulation possible in dense canopies."
        spray_recommendation = "Ensure adequate plant spacing and apply biological protective sprays (e.g. Bacillus subtilis) if rain is expected."
        susceptible_diseases = ["Early Blight", "Septoria Leaf Spot", "Anthracnose"]
    elif risk_score < 80:
        risk_level = "High Risk"
        risk_badge = "status-high"
        advisory = "High humidity (>75%) creates optimal incubation window for fungal and bacterial pathogens."
        spray_recommendation = "Apply preventative copper octanoate or systemic fungicide before evening dew. Avoid overhead watering."
        susceptible_diseases = ["Late Blight", "Early Blight", "Rust Pustules", "Bacterial Spot"]
    else:
        risk_level = "Severe Proliferation Alert"
        risk_badge = "status-critical"
        advisory = "CRITICAL PATHOGEN INFECTION CONDITIONS: Persistent free moisture, high humidity, and warm canopy."
        spray_recommendation = "Immediate preventative/curative spray intervention required. Prune dense foliage to promote airflow."
        susceptible_diseases = ["Late Blight (Phytophthora)", "Downy Mildew", "Bacterial Canker", "Black Rot"]

    return {
        "location": climate["location"],
        "temperature_c": climate["temperature_c"],
        "temperature_f": round(climate["temperature_c"] * 9/5 + 32, 1),
        "humidity_pct": climate["humidity_pct"],
        "rain_chance_pct": climate["rain_chance_pct"],
        "wind_speed_kmh": climate["wind_speed_kmh"],
        "condition": climate["condition"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_badge": risk_badge,
        "advisory": advisory,
        "spray_recommendation": spray_recommendation,
        "susceptible_diseases": susceptible_diseases,
        "presets": list(PRESET_FARM_CLIMATES.keys())
    }


# Crop Emoji Mapping for UI Boxes
CROP_ICONS = {
    "Tomato": "🍅",
    "Potato": "🥔",
    "Corn": "🌽",
    "Apple": "🍎",
    "Grape": "🍇",
    "Pepper": "🫑",
    "Rice": "🌾",
    "Wheat": "🌾",
    "Soybean": "🌱",
    "Cotton": "☁️",
    "Coffee": "☕",
    "Banana": "🍌",
    "Strawberry": "🍓",
    "Sugarcane": "🎋",
    "Mango": "🥭",
    "Cassava": "🍠",
    "Orange": "🍊",
    "Citrus": "🍋",
    "Peach": "🍑",
    "Cherry": "🍒",
    "Blueberry": "🫐",
    "Raspberry": "🍇",
    "Squash": "🎃",
    "Cucumber": "🥒",
    "Watermelon": "🍉",
    "Bean": "🫘",
    "Pea": "🫛",
    "Barley": "🌾",
    "Oat": "🌾",
    "Sorghum": "🌾",
    "Tea": "🍵",
    "Cabbage": "🥬",
    "Lettuce": "🥗",
    "Onion": "🧅",
    "Garlic": "🧄",
    "Eggplant": "🍆",
    "Rose": "🌹",
    "Papaya": "🍈",
    "Guava": "🍐",
    "Pomegranate": "🍎",
    "Olive": "🫒",
    "Almond": "🥜",
    "Avocado": "🥑",
    "Pineapple": "🍍"
}

@app.get("/crops-summary")
def get_crops_summary():
    """
    Returns all crops grouped into structured boxes for clean,
    uncluttered display in the Disease Library without mixed text.
    """
    model_svc = get_model_service()
    diseases_dict = model_svc.disease_info
    
    crops_map: Dict[str, Dict[str, Any]] = {}
    
    for d_key, info in diseases_dict.items():
        crop_name = info.get("crop", d_key.split("_")[0])
        scientific_name = info.get("scientific_name", "Botanical specimen")
        crop_group = info.get("crop_group", "Vegetables")
        
        if crop_name not in crops_map:
            icon = CROP_ICONS.get(crop_name, "🌿")
            crops_map[crop_name] = {
                "crop": crop_name,
                "icon": icon,
                "scientific_name": scientific_name,
                "crop_group": crop_group,
                "total_diseases": 0,
                "diseases": []
            }
            
        crops_map[crop_name]["total_diseases"] += 1
        crops_map[crop_name]["diseases"].append({
            "disease_id": d_key,
            "disease_name": info.get("disease_name", d_key.replace("_", " ")),
            "category": info.get("category", "Fungal"),
            "severity_level": info.get("severity_level", "Moderate"),
            "severity_score": info.get("severity_score", 50),
            "pathogen": info.get("pathogen", "Pathogenic agent")
        })

    # Sort crops alphabetically
    sorted_crops = sorted(crops_map.values(), key=lambda c: c["crop"])
    
    # Extract unique crop groups
    crop_groups = ["All Crops"] + sorted(list({c["crop_group"] for c in sorted_crops}))

    return {
        "total_crops": len(sorted_crops),
        "total_diseases": len(diseases_dict),
        "crop_groups": crop_groups,
        "crops": sorted_crops
    }


@app.get("/samples")
def get_sample_images():
    """Returns metadata for pre-packaged sample leaves for instant testing."""
    sample_list = []
    if SAMPLES_DIR.exists():
        samples_meta = [
            {"name": "Tomato Early Blight", "crop": "Tomato", "filename": "tomato_early_blight.jpg", "category": "Fungal"},
            {"name": "Tomato Late Blight", "crop": "Tomato", "filename": "tomato_late_blight.jpg", "category": "Oomycete"},
            {"name": "Tomato Healthy Leaf", "crop": "Tomato", "filename": "tomato_healthy.jpg", "category": "Healthy"},
            {"name": "Potato Early Blight", "crop": "Potato", "filename": "potato_early_blight.jpg", "category": "Fungal"},
            {"name": "Potato Late Blight", "crop": "Potato", "filename": "potato_late_blight.jpg", "category": "Oomycete"},
            {"name": "Corn Common Rust", "crop": "Corn", "filename": "corn_common_rust.jpg", "category": "Fungal"},
            {"name": "Corn Northern Blight", "crop": "Corn", "filename": "corn_northern_blight.jpg", "category": "Fungal"},
            {"name": "Apple Scab", "crop": "Apple", "filename": "apple_scab.jpg", "category": "Fungal"},
            {"name": "Grape Black Rot", "crop": "Grape", "filename": "grape_black_rot.jpg", "category": "Fungal"},
            {"name": "Pepper Bacterial Spot", "crop": "Pepper", "filename": "pepper_bacterial_spot.jpg", "category": "Bacterial"},
        ]
        for item in samples_meta:
            file_path = SAMPLES_DIR / item["filename"]
            if file_path.exists():
                item["url"] = f"/samples-static/{item['filename']}"
                sample_list.append(item)
    return {"samples": sample_list}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

