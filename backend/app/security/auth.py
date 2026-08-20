import hashlib
import hmac
import base64
import json
import time
import os
from typing import Optional, Dict, Any
from app.config import settings
from app.database.database import get_db_connection
from app.database.schemas import UserRole

def hash_password(password: str) -> str:
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"{base64.b64encode(salt).decode('utf-8')}${base64.b64encode(key).decode('utf-8')}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        salt_b64, key_b64 = hashed_password.split('$')
        salt = base64.b64decode(salt_b64)
        expected_key = base64.b64decode(key_b64)
        new_key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000)
        return hmac.compare_digest(expected_key, new_key)
    except Exception:
        return False

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _b64url_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)

def create_access_token(data: Dict[str, Any], expires_delta_seconds: Optional[int] = None) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = data.copy()
    now = int(time.time())
    exp = now + (expires_delta_seconds or (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60))
    payload.update({"iat": now, "exp": exp})
    
    header_b64 = _b64url_encode(json.dumps(header, separators=(',', ':')).encode('utf-8'))
    payload_b64 = _b64url_encode(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    
    signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
    signature = hmac.new(settings.SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()
    sig_b64 = _b64url_encode(signature)
    
    return f"{header_b64}.{payload_b64}.{sig_b64}"

def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts
        
        signature_input = f"{header_b64}.{payload_b64}".encode('utf-8')
        expected_sig = hmac.new(settings.SECRET_KEY.encode('utf-8'), signature_input, hashlib.sha256).digest()
        provided_sig = _b64url_decode(sig_b64)
        
        if not hmac.compare_digest(expected_sig, provided_sig):
            return None
        
        payload_bytes = _b64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        if payload.get('exp', 0) < int(time.time()):
            return None  # Expired
            
        return payload
    except Exception:
        return None

def seed_default_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    if cursor.fetchone()['count'] == 0:
        users = [
            ("admin", "admin@qshield.security", hash_password("Admin@QShield2026!"), UserRole.ADMIN.value),
            ("analyst", "analyst@qshield.security", hash_password("Analyst@QShield2026!"), UserRole.ANALYST.value),
            ("viewer", "viewer@qshield.security", hash_password("Viewer@QShield2026!"), UserRole.VIEWER.value)
        ]
        cursor.executemany("""
        INSERT INTO users (username, email, password_hash, role, created_at)
        VALUES (?, ?, ?, ?, datetime('now'))
        """, users)
        conn.commit()
    conn.close()
