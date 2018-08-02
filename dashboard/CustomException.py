from rest_framework.exceptions import APIException


class EmailAlreadyRegistered(APIException):
    status_code = 800
    default_detail = "Email already registered with us "
    default_code = "Operation not permitted"


class UnknownProblem(APIException):
    status_code = 900
    default_detail = "Some problem occured "
    default_code = "Server Error"
