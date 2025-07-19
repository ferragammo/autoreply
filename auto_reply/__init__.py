from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException


def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def read_root():
        return {"report": "Hello world!"}

    return app
