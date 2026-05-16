from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def hello() -> dict:
    """Return a greeting message."""
    return {"message": "Hello from FastAPI!"}
