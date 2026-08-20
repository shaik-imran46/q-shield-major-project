from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from app.database.schemas import UserCreate, UserLogin, UserResponse, Token, UserRole
from app.database.database import get_db_connection
from app.security.auth import hash_password, verify_password, create_access_token, verify_access_token
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (user.username, user.email))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username or email already registered")
        
    pwd_hash = hash_password(user.password)
    now = datetime.utcnow().isoformat()
    cursor.execute("""
    INSERT INTO users (username, email, password_hash, role, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (user.username, user.email, pwd_hash, user.role.value, now))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return UserResponse(
        id=user_id,
        username=user.username,
        email=user.email,
        role=user.role,
        created_at=now
    )

@router.post("/login", response_model=Token)
def login_user(creds: UserLogin):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (creds.username,))
    row = cursor.fetchone()
    conn.close()
    
    if not row or not verify_password(creds.password, row['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    user_resp = UserResponse(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        role=UserRole(row['role']),
        created_at=row['created_at']
    )
    
    token = create_access_token({"sub": user_resp.username, "role": user_resp.role.value, "id": user_resp.id})
    return Token(access_token=token, token_type="bearer", user=user_resp)

@router.get("/me", response_model=UserResponse)
def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        # Return default analyst identity for guest / exploration mode
        return UserResponse(id=1, username="analyst", email="analyst@qshield.security", role=UserRole.ANALYST, created_at=datetime.utcnow().isoformat())
        
    token = authorization.split(" ")[1]
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired authentication token")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (payload['sub'],))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="User not found")
        
    return UserResponse(
        id=row['id'],
        username=row['username'],
        email=row['email'],
        role=UserRole(row['role']),
        created_at=row['created_at']
    )
