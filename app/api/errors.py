from fastapi import HTTPException, status

class APIError(HTTPException):
    
    def __init__(self, 
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, 
        detail: str = "An internal server error occurred."
    ):
        super().__init__(
            status_code=status_code, 
            detail=detail
        )

class NotFoundError(APIError):
    def __init__(self, detail: str = "Resource not found."):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)