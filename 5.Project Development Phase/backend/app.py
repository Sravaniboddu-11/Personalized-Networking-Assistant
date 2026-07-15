from fastapi import FastAPI
from pydantic import BaseModel
from backend.theme_extractor import extract_themes
from backend.feedback import save_feedback
from backend.models import FeedbackRequest
from backend.generator import generate_conversation_starters
from backend.database import create_database, save_conversation, get_history
from backend.wiki_service import get_wikipedia_summary

app = FastAPI(
    title="Personalized Networking Assistant",
    description="AI-powered assistant for networking events",
    version="1.0.0"
)

# Create database
create_database()


# -----------------------------
# Request Models
# -----------------------------
class ConversationRequest(BaseModel):
    event: str
    interests: str


class FactCheckRequest(BaseModel):
    topic: str


# -----------------------------
# Home API
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to Personalized Networking Assistant!",
        "status": "Backend is running successfully."
    }


# -----------------------------
# Generate Conversation Starters
# -----------------------------
@app.post("/generate")
def generate(request: ConversationRequest):

    # Extract themes
    themes = extract_themes(request.event)

    # Generate conversation starters
    starters = generate_conversation_starters(
        request.event,
        request.interests
    )

    if isinstance(starters, str):
        starters = [starters]

    # Save to database
    for starter in starters:
        save_conversation(
            request.event,
            request.interests,
            starter
        )

    return {
        "event": request.event,
        "themes": themes,
        "interests": request.interests,
        "conversation_starters": starters
    }


# -----------------------------
# History API
# -----------------------------
@app.get("/history")
def history():

    data = get_history()

    return {
        "history": data
    }
@app.post("/feedback")
def feedback(request: FeedbackRequest):

    save_feedback(
        request.conversation_id,
        request.feedback
    )

    return {
        "message": "Feedback saved successfully"
    }



# -----------------------------
# Wikipedia Fact Check API
# -----------------------------
@app.post("/factcheck")
def factcheck(request: FactCheckRequest):

    result = get_wikipedia_summary(request.topic)

    return result