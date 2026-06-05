from fastapi import FastAPI
from app.api.upload import router as upload_router
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address
)

app = FastAPI()
app.include_router(upload_router)
app.state.limiter = limiter

@app.get("/")
def health():
    return {"status": "ok"}

