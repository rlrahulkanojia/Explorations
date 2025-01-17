"""API Service router."""

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from service.commons.auth import Validator
from service.endpoints.v1.cloth import get_cloth

validate_token = Validator()

api_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
    dependencies=[Depends(validate_token)],
)

api_router.add_api_route(
    methods=["POST"],
    path="/get-cloth",
    endpoint=get_cloth,
    status_code=HTTP_200_OK
)
