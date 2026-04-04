from fastapi import FastAPI
from routes.car_route import router
from routes import webhook_route
from middleware.auth import APIKeyMiddleware

app = FastAPI()

app.add_middleware(APIKeyMiddleware)

app.include_router(router)
app.include_router(webhook_route.router)