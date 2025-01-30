from pyexpat.errors import messages
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..models.message import Message
from ..schemas.message import MessageCreate,Messege_get,MessageResponse


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
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from ..models.message import Message
from ..schemas.message import Messege_get, MessageResponse  # Assuming you have these schemas
from typing import List

def get_all_message(db: Session, message: Messege_get) -> list[Message]:
    try:
        # Querying for messages based on the user_id
        message_list = db.query(Message).filter(Message.user_id == message.user_id).all()

        if not message_list:
            # If no messages are found, return a 404 response
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "No messages found for this user"}
            )

        # Return the list of messages
        # Converting the messages to the MessageResponse schema
        return message_list

        return JSONResponse(
            status_code=200,
            content={"status": "success", "data": response_data},
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": f"An error occurred: {str(e)}"},
        )
