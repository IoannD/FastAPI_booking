from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User already exist'


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Incorrect email or password'


class TokenExpiredException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Token expired'


class TokenAbsentException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Token absence'


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Incorrect token format'


class UserIsNotPresentException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = ''


class RoomCannotBeBookedException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'There are no available rooms left'
