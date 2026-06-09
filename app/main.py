from fastapi import FastAPI
from fastapi import APIRouter
from app.api.upload import router as upload_router
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.agents.advisor import generate_financial_advice
import json

limiter = Limiter(
    key_func=get_remote_address
)

app = FastAPI()
router = APIRouter()

app.include_router(upload_router)
app.state.limiter = limiter



@app.get("/")
def health():
    return {"status": "ok"}


@router.get("/test/{name}")
def test(name:str):
    path = (
        f"app/documents/"
        f"{name}_analytics.json"
    )

    with open(path) as f:
        analytics = json.load(f)

    advice = generate_financial_advice(
        analytics
    )

    return {
        "analytics": analytics,
        "advice": advice
    }

app.include_router(router)