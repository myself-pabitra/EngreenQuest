import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import get_settings
from app.core.logging_conf import LOGGING_CONFIG   # noqa: F401  (side-effect)
from app.api.v1.routes_contact import router as contact_router
from fastapi.middleware.cors import CORSMiddleware


settings = get_settings()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url="/v1/openapi.json",
    docs_url="/v1/docs",
    root_path="/api/engreenquest"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],              # or use ["*"] to allow all (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],                # allow all HTTP methods
    allow_headers=["*"],                # allow all headers
)

# Routers
app.include_router(contact_router, prefix=settings.API_V1_STR)

# Global error handler for 422 validation errors
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # Let FastAPI handle its own; we just standardise the payload structure
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Custom handler for generic exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logging.getLogger("uvicorn.error").exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error – our team has been notified."},
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, workers=1)

