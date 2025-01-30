from pyexpat.errors import messages
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..models.message import Message
from ..schemas.message import MessageCreate


def store_message(db: Session, message: MessageCreate):

    try:
        db_message = Message(
            user_id=message.user_id,
            message=message.message,
            is_bot=message.is_bot
        )

        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return JSONResponse(
            status_code=201,
            content={"status": "success", "message": "Response stored", "response_id": db_message.id},
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": "An error occurred while storing the response"},
        )
