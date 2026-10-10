import os
import sys
from dotenv import dotenv_values, load_dotenv

load_dotenv(".env")
raw_config = dotenv_values(".env")

print("=" * 60)
print("ENVIRONMENT CONFIGURATION AUDIT REPORT")
print("=" * 60)

PLACEHOLDER_SUBSTRINGS = ["placeholder", "paste", "replace", "your-", "user:password", "<", ">"]

def check_placeholder(val: str | None) -> bool:
    if not val:
        return False
    v_lower = val.lower()
    return any(p in v_lower for p in PLACEHOLDER_SUBSTRINGS)

# 1. Variable Presence & Placeholder Check
variables = ["DATABASE_URL", "SECRET_KEY", "ALGORITHM", "ACCESS_TOKEN_EXPIRE_MINUTES", "GEMINI_API_KEY"]

for var in variables:
    val = raw_config.get(var)
    if not val or not val.strip():
        status = "MISSING / EMPTY"
    elif check_placeholder(val):
        status = "PLACEHOLDER DETECTED (Manual entry required)"
    else:
        status = "CONFIGURED (Custom value set)"
    print(f"[{var}]: {status}")

print("-" * 60)

# 2. JWT Configuration Check
secret = os.getenv("SECRET_KEY")
algo = os.getenv("ALGORITHM", "HS256")
if not secret or check_placeholder(secret):
    print("JWT Signing: PENDING (SECRET_KEY contains placeholder)")
else:
    try:
        from jose import jwt
        token = jwt.encode({"test": "value"}, secret, algorithm=algo)
        decoded = jwt.decode(token, secret, algorithms=[algo])
        if decoded.get("test") == "value":
            print("JWT Signing: SUCCESS (Valid secret & algorithm)")
        else:
            print("JWT Signing: FAILED (Decoding mismatch)")
    except Exception as e:
        print(f"JWT Signing: FAILED ({type(e).__name__})")

# 3. Database Connectivity Check
db_url = os.getenv("DATABASE_URL")
if not db_url or check_placeholder(db_url):
    print("Database Connection: PENDING (DATABASE_URL contains placeholder)")
else:
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(db_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database Connection: SUCCESS (Connected to PostgreSQL)")
    except Exception as e:
        print(f"Database Connection: FAILED ({type(e).__name__})")

# 4. Gemini AI Check
gemini_key = os.getenv("GEMINI_API_KEY")
if not gemini_key or check_placeholder(gemini_key):
    print("Gemini AI API: PENDING (GEMINI_API_KEY contains placeholder)")
else:
    try:
        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-pro")
        resp = model.generate_content("Ping")
        if resp and resp.text:
            print("Gemini AI API: SUCCESS (Live response received)")
        else:
            print("Gemini AI API: FAILED (Empty response)")
    except Exception as e:
        print(f"Gemini AI API: FAILED ({type(e).__name__})")

print("=" * 60)
