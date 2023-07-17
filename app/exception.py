from fastapi import HTTPException, status


# UserAlreadyExistException = HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                           detail='User already exist')

# IncorrectEmailOrPasswordException = HTTPException(
#     status_code=status.HTTP_409_CONFLICT, detail='Incorrect email or password')

# TokenExpiredException = HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                       detail='Token expired')

# TokenAbsentException = HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                       detail='Token absence')

# IncorrectTokenFormatException = HTTPException(status_code=status.HTTP_409_CONFLICT,
#                                       detail='Incorrect token format')

# UserIsNotPresentException = HTTPException(status_code=status.HTTP_409_CONFLICT)


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
