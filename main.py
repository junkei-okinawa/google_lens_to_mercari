from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from app.controllers import main_controller

import logging

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Google Lens to Mercari Tool")

# Trust proxy headers (for Cloud Run HTTPS)
# Cloud Run (via Google Front End) strips untrusted X-Forwarded-* headers from external requests,
# so trusting "*" is safe and necessary to correctly detect HTTPS protocol.
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routes
app.include_router(main_controller.router)

if __name__ == "__main__":
    import uvicorn

    # Cloud Run sets PORT env var, but uvicorn in Dockerfile uses this as fallback/dev
    # Production run command in Dockerfile overrides this anyway
    uvicorn.run(app, host="0.0.0.0", port=8000)
