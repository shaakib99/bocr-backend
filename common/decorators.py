from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def responsify(func):

    def __inner(*args):
        try:
            data = func(*args)
            status_code = HTTP_200_OK

            if 'status_code' in data:
                status_code = data['status_code']
                del data['status_code']
            return Response(data=data, status=status_code)

        except Exception as e:
            status_code = HTTP_400_BAD_REQUEST
            detail = 'undefined'
            if hasattr(e, 'status_code'):
                status_code = e.status_code
            if hasattr(e, 'detail'):
                detail = e.detail

            return Response(data=detail, status=status_code)

    return __inner
