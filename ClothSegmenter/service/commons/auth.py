"""AWS Cognito Token validation."""
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from service.commons.logger import get_logger

log = get_logger(__name__)

class Validator(HTTPBearer):
    """
    Dummy function to validate tokens.

    Inherits from HTTPBearer to handle Bearer token authentication.
    """
    def __init__(self, auto_error: bool = True):
        """
        Initialize the Validator.

        Args:
            auto_error (bool): Whether to automatically raise an error on invalid credentials.
        """
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        """
        Validate the JWT token from the request.

        Args:
            request (Request): The FastAPI request object.

        Returns
        -------
            dict: The decoded JWT payload.

        Raises
        ------
            HTTPException: If the token is invalid or expired.
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme."
            )
        try:
            payload = True

        except Exception as e:
            log.error(f"Unexpected error during token validation: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred during authentication: {e}")

        if payload:
            return credentials
        
        return None
