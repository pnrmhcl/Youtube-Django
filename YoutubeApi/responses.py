from wsgiref.util import FileWrapper

from rest_framework.response import Response

ERROR_MESSAGES = {

    100: "Something went wrong",

}


def response_200(data=None):
    return Response({
        "error": False,
        "errorMsg": "completed",
        "errorCode": 200,
        "data": data
    }, status=200)


def response_400(data=None):
    return Response({
        "error": True,
        "errorMsg": "Request not valid",
        "errorCode": 400,
        "data": data
    }, status=400)


def response_500(error_code, data=None):
    return Response({
        "error": True,
        "errorMsg": ERROR_MESSAGES[error_code],
        "errorCode": error_code,
        "data": data
    }, status=500)


def response_403():
    return Response({
        "error": True,
        "errorMsg": "Not authorized",
        "errorCode": 403,
        "data": None
    }, status=403)
