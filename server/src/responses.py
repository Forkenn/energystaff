from fastapi import Response, status
from src.exceptions import SException

response_204 = Response(status_code=status.HTTP_204_NO_CONTENT)

openapi_exception = {"model": SException}
openapi_204 = {status.HTTP_204_NO_CONTENT: {}}
openapi_404 = {status.HTTP_404_NOT_FOUND: openapi_exception}
openapi_400 = {status.HTTP_400_BAD_REQUEST: openapi_exception}
