"""
Authentication endpoints for the High School Management System API
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import hashlib
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from ..database import teachers_collection

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash, trying both Argon2 and SHA-256"""
    # Try Argon2 first (used in database.py)
    try:
        ph = PasswordHasher()
        ph.verify(hashed_password, password)
        return True
    except (VerifyMismatchError, Exception):
        pass
    
    # Fall back to SHA-256
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    return sha256_hash == hashed_password

@router.post("/login")
def login(username: str, password: str) -> Dict[str, Any]:
    """Login a teacher account"""
    # Find the teacher in the database
    teacher = teachers_collection.find_one({"_id": username})
    
    if not teacher or not verify_password(password, teacher["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Return teacher information (excluding password)
    return {
        "username": teacher["username"],
        "display_name": teacher["display_name"],
        "role": teacher["role"]
    }

@router.get("/check-session")
def check_session(username: str) -> Dict[str, Any]:
    """Check if a session is valid by username"""
    teacher = teachers_collection.find_one({"_id": username})
    
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    return {
        "username": teacher["username"],
        "display_name": teacher["display_name"],
        "role": teacher["role"]
    }