from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import districts, constituencies, candidates, ranking

app = FastAPI(
    title="Know Your Candidate API",
    description="Kerala Election Decision Support System — explore, compare, and rank candidates dynamically.",
    version="1.0.0",
)

# CORS — allow frontend origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(districts.router)
app.include_router(constituencies.router)
app.include_router(candidates.router)
app.include_router(ranking.router)


@app.get("/")
def root():
    return {
        "name": "Know Your Candidate API",
        "version": "1.0.0",
        "description": "Kerala Election Decision Support System",
        "endpoints": [
            "GET /districts",
            "GET /constituencies?district=<name>",
            "GET /candidates?district=<name>&constituency=<name>",
            "GET /candidate/<id>",
            "GET /candidate/<id>/news",
            "POST /rank",
        ],
    }
