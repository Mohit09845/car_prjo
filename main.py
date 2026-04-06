import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI

# Load .env before any sub-module is imported so every os.getenv() call
# in database/connection.py, intent_parser.py, etc. sees the values.
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup / shutdown lifecycle hook.
    Runs once when the server starts — before the first request is served.
    """
    # ── Validate required environment variables ───────────────────────────────
    required_vars = ["MONGO_URL", "API_KEY", "NVIDIA_API_KEY"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        raise RuntimeError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Check your .env file or Docker environment config."
        )

    print("✅ Environment variables validated.")

    # Safely connect and ensure DB indexes ONLY after env vars are fully validated
    from database.connection import ensure_indexes
    from fastapi.concurrency import run_in_threadpool
    await run_in_threadpool(ensure_indexes)
    
    print("🚀 Car API is starting up…")

    yield  # ← application runs here

    print("🛑 Car API is shutting down.")


from routes.car_route import router
from routes import webhook_route
from middleware.auth import APIKeyMiddleware

app = FastAPI(
    lifespan=lifespan,
    title="Maruti Suzuki Car API",
    description=(
        "Intent-driven REST API powering an ElevenLabs AI voice assistant "
        "for a Maruti Suzuki dealership. Provides car lookup, variant comparison, "
        "price-range filtering, and an NLP webhook endpoint."
    ),
    version="1.0.0",
)

app.add_middleware(APIKeyMiddleware)

app.include_router(router)
app.include_router(webhook_route.router)