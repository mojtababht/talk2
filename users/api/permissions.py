from rest_framework.exceptions import APIException
from rest_framework import status


class NeedToNotAuthenticate(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = 'need_to_not_authenticate'
