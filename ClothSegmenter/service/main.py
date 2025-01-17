"""API module with Cloth endpoints."""
from fastapi import Depends, FastAPI
from starlette.status import HTTP_200_OK

from service.commons.auth import Validator
from service.commons.environment import ENVIRONMENT, SERVICE_VERSION
from service.commons.logger import get_logger
from service.routers.v1.router import api_router

log = get_logger(__name__)

app = FastAPI(
    title="Cloth Segmenter Endpoint : Modelia",
    description="API for U2Net based cloth Segmenter.",
    version=SERVICE_VERSION,
    redoc_url=None,
    docs_url="/docs",
)

validate_token = Validator()
app.include_router(api_router)

@app.get("/", status_code=HTTP_200_OK, dependencies=[Depends(validate_token)])
def root():
    """Root API path.

    Returns
    -------
    dict
        Returns service environment and version
    """
    log.info("Get request at /")
    return {
        "message": "cloth-segmenter-api",
        "version": SERVICE_VERSION,
        "environment": ENVIRONMENT,
    }

@app.get("/health", status_code=HTTP_200_OK)
def health():
    """Endpoint to check if the application is up and running."""
    log.info("Get request at /health")
    return None


@app.get("/ready", status_code=HTTP_200_OK)
def ready():
    """Endpoint to check if the application is ready to serve requests."""
    log.info("Get request at /ready")
    return None


