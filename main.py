from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers import main_controller

import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Google Lens to Mercari Tool")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
app.include_router(main_controller.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
