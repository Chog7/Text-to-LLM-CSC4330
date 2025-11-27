# app/whatsapp_controller.py

from fastapi import APIRouter, Form, Response, status
from twilio.twiml.messaging_response import MessagingResponse

from . import llm_service  # adjust to your actual file / function

router = APIRouter(prefix="/whatsapp", tags=["whatsapp"])


@router.post("/webhook")
async def whatsapp_webhook(
    From: str = Form(...),  # e.g. "whatsapp:+1234567890"
    Body: str = Form(...),  # the text they sent
):
    """
    Twilio WhatsApp Sandbox will POST here whenever someone sends a WhatsApp
    message to your sandbox number.

    We:
      - read the message text
      - call the LLM
      - respond with TwiML so Twilio sends a WhatsApp reply back.
    """
    user_text = Body

    # Call your existing LLM logic.
    # If your function is named differently, change this line:
    reply_text = await llm_service.generate_response(user_text)

    twiml = MessagingResponse()
    twiml.message(reply_text)

    return Response(
        content=str(twiml),
        media_type="application/xml",
        status_code=status.HTTP_200_OK,
    )
