import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

# Routes that don't require an API key
PUBLIC_ROUTES = ["/docs", "/openapi.json", "/redoc"]


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # ── skip public routes ────────────────────────────────────────────────
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)

        # ── check header ──────────────────────────────────────────────────────
        api_key = request.headers.get("X-API-Key")

        if not api_key:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing API key. Add 'X-API-Key' to your request headers."},
            )

        # ── validate against .env ─────────────────────────────────────────────
        if api_key != os.getenv("API_KEY"):
            return JSONResponse(
                status_code=403,
                content={"detail": "Invalid API key."},
            )

        # ── valid — pass to route ─────────────────────────────────────────────
        return await call_next(request)