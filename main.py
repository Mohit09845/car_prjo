from fastapi import FastAPI
from routes.car_route import router
from middleware.auth import APIKeyMiddleware

app = FastAPI()

app.add_middleware(APIKeyMiddleware)
app.include_router(router)