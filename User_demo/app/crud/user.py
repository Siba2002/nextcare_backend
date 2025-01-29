from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse



from ..models.user import User
from ..schemas.user import UserCreate
import bcrypt


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def verify_password(stored_hash: str, password: str) -> bool:
    """Verifies a password against a stored hash."""
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))


def create_user(db: Session, user: UserCreate):
    """Creates a new user in the database with proper error handling and JSON response format."""
    try:
        hashed_password = hash_password(user.password)
        db_user = User(
            name=user.name,
            mobile=user.mobile,
            password=hashed_password,
            dob=user.dob,
            gender=user.gender,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": "User created", "user_id": db_user.id},
        )

    except IntegrityError:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "Database error while creating user"},
        )

    except Exception:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "An unexpected error occurred"},
        )



def login_user(db: Session, mobile: str, password: str) -> JSONResponse:
    """Logs in a user by verifying credentials and returns appropriate status codes."""
    db_user = db.query(User).filter(User.mobile == mobile).first()

    if not db_user:
        return JSONResponse(content={"error": "Invalid credentials"}, status_code=401)

    if not verify_password(db_user.password, password):
        return JSONResponse(content={"error": "Password mismatch"}, status_code=401)

    return JSONResponse(
        content={"message": f"Hello {db_user.name}, successfully logged in"},
        status_code=200
    )

