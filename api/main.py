from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="University Dropout Prediction API",
    description="API de prédiction du risque de décrochage universitaire",
    version="1.0.0"
)

app.include_router(router)