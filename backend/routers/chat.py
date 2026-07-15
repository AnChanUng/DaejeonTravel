from fastapi import APIRouter

from chatbot.schema import ChatRequest, ChatResponse
from chatbot.service import ask_chatbot

router = APIRouter(
    prefix="/api",
    tags=["chatbot"]
)


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = ask_chatbot(request.message)

    return ChatResponse(answer=answer)