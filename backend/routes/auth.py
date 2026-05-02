from fastapi import APIRouter, HTTPException, Depends
from datetime import timedelta
from schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from database import get_db
from utils import hash_password, verify_password, create_access_token, extract_user_id_from_token

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserRegister, db = Depends(get_db)):
    """Register a new user"""
    db.connect()
    
    # Check if user already exists
    query = "SELECT id FROM users WHERE username = %s OR email = %s"
    existing_user = db.execute_single(query, (user.username, user.email))
    
    if existing_user:
        db.disconnect()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    # Hash password
    password_hash = hash_password(user.password)
    
    # Insert user
    query = """
    INSERT INTO users (username, email, password_hash, first_name, last_name, target_exam)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id, username, email, first_name, last_name, target_exam, created_at
    """
    params = (user.username, user.email, password_hash, user.first_name, user.last_name, user.target_exam)
    new_user = db.execute_single(query, params)
    db.disconnect()
    
    if not new_user:
        raise HTTPException(status_code=400, detail="Failed to create user")
    
    return UserResponse(**dict(new_user))

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db = Depends(get_db)):
    """Login user and return JWT token"""
    db.connect()
    
    # Get user by username
    query = "SELECT id, username, email, password_hash, first_name, last_name, target_exam, created_at FROM users WHERE username = %s"
    user = db.execute_single(query, (credentials.username,))
    db.disconnect()
    
    if not user or not verify_password(credentials.password, user['password_hash']):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Create token
    access_token = create_access_token(
        data={"sub": str(user['id'])},
        expires_delta=timedelta(days=7)
    )
    
    user_response = UserResponse(
        id=user['id'],
        username=user['username'],
        email=user['email'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        target_exam=user['target_exam'],
        created_at=user['created_at']
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=user_response
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(authorization: str = None, db = Depends(get_db)):
    """Get current user info from token"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Extract token from "Bearer <token>"
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    user_id = extract_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db.connect()
    query = "SELECT id, username, email, first_name, last_name, target_exam, created_at FROM users WHERE id = %s"
    user = db.execute_single(query, (user_id,))
    db.disconnect()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(**dict(user))

@router.post("/verify-token")
def verify_token(authorization: str = None):
    """Verify if token is valid"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    user_id = extract_user_id_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return {"valid": True, "user_id": user_id}
