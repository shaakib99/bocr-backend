from urllib.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from helper.util import jwtDecode
from rest_framework.exceptions import NotAuthenticated


def responsify(func):

    def __inner(*args):
        try:
            data = func(*args)
            status_code = HTTP_200_OK

            if data and 'status_code' in data:
                status_code = data['status_code']
                del data['status_code']
            return Response(data=data, status=status_code)

        except Exception as e:
            status_code = HTTP_400_BAD_REQUEST
            detail = e.__repr__()
            if hasattr(e, 'status_code'):
                status_code = e.status_code
            if hasattr(e, 'detail'):
                detail = e.detail

            return Response(data=detail, status=status_code)

    return __inner


def jwtAuthGuard(func):

    def __inner(*args):
        request: Request = args[0]
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                user = jwtDecode(token)
                if not user:
                    raise NotAuthenticated('User is not authenticated')
                return func(*args, user)
            except Exception as e:
                print(e.__repr__())
                raise NotAuthenticated('User is not authenticated')

    return __inner


def jwtAuthGuardExcept(func):

    def __inner(*args):
        request: Request = args[0]
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                user = jwtDecode(token)
                if not user:
                    raise NotAuthenticated('User is not authenticated')
                return func(*args, user)
            except Exception as e:
                raise e
        else:
            return func(*args)

    return __inner