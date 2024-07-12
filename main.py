from fastapi import FastAPI
from app.api.v1.weather import router as weather_router

app = FastAPI()

app.include_router(weather_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
