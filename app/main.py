from fastapi import FastAPI

from app.controllers.user import router as user_router

app = FastAPI(title="Lost and Found API")

app.include_router(user_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
