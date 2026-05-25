from fastapi import APIRouter
from pydantic import BaseModel

from app.graph.workflow import run_workflow

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):

    result = run_workflow(request.message)

    return result