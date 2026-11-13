import logging
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.agent import ask_agent

logging.basicConfig(
    filename="assistant_audit.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("enterprise_assistant")

app = FastAPI(title="Enterprise Data Q&A Assistant",
              description="Ask questions about SQLite and CSV data.",
              version="1.0.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)

class AskResponse(BaseModel):
    answer: str
    timestamp: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        answer = ask_agent(request.question)
        logger.info("question=%r answer=%r", request.question, answer)
        return AskResponse(answer=answer,
                           timestamp=datetime.now(timezone.utc).isoformat())
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        logger.exception("Assistant request failed")
        raise HTTPException(status_code=500,
                            detail="The assistant could not process this request.")
