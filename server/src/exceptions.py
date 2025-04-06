from pydantic import BaseModel
from fastapi import HTTPException, status


class SException(BaseModel):
    detail: str


class UnsupportedMediaException(HTTPException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    detail = ''

    def __init__(self, headers = None):
        super().__init__(self.status_code, self.detail, headers)


class BadRequestException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = ''

    def __init__(self, headers = None):
        super().__init__(self.status_code, self.detail, headers)


class ForbiddenException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'FORBIDDEN'

    def __init__(self, headers = None):
        super().__init__(self.status_code, self.detail, headers)


class NotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'ITEM_NOT_FOUND'

    def __init__(self, headers = None):
        super().__init__(self.status_code, self.detail, headers)


class FileTypeException(UnsupportedMediaException):
    detail = 'INVALID_FILE_TYPE'


class FIleParamsException(UnsupportedMediaException):
    detail = 'INVALID_FILE_PARAMS'


class AlreadyExistException(BadRequestException):
    detail = 'OBJECT_ALREADY_EXIST'


class YourselfException(BadRequestException):
    detail = 'CAN_NOT_DONE_ON_YOURSELF'


class BannedException(BadRequestException):
    detail = 'REQUESTED_OBJECT_BANNED'


class MaxObjectsException(BadRequestException):
    detail = 'MAX_OBJECTS_COUNT_IN_DB'


class NotAllowedException(ForbiddenException):
    detail = 'NOT_ALLOWED'
