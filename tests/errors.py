class APIError(object):
    def __init__(self, code, msg, status_code=200):
        self.code = code
        self.msg = msg
        self.status_code = status_code

    def as_response(self):
        response = {'error_code': self.code, 'error_msg': self.msg}
        return response


UNAUTHORIZED = APIError(10001, msg='unauthorized')
UNAUTHORIZED_IP = APIError(10002, msg='unauthorized ip')
INVALID_API_ID = APIError(10003, msg='invalid api id')
INVALID_API_KEY = APIError(10004, msg='invalid api key')
AUTHENTICATION_FAILED = APIError(10005, msg='authentication failed')
INSUFFICIENT_RESOURCES = APIError(10006, msg='insufficient resources')
API_USER_EXPIRED = APIError(10007, msg='api user expired')
INVALID_JSON = APIError(10101, msg='invalid json')
INVALID_PAGE = APIError(10102, msg='invalid page')
INVALID_SIZE = APIError(10103, msg='invalid size')
INVALID_IP = APIError(10104, msg='invalid ip')
INVALID_DOMAIN = APIError(10105, msg='invalid domain')
INVALID_HOST = APIError(10106, msg='invalid host')
INVALID_VALUE_IP = APIError(10107, msg='invalid value_ip')
INVALID_VALUE_DOMAIN = APIError(10108, msg='invalid value_domain')
INVALID_VALUE_HOST = APIError(10109, msg='invalid value_host')
INVALID_EMAIL = APIError(10110, msg='invalid email')
REQUIRE_SCAN_ID = APIError(10111, msg='require scan_id')
INVALID_SCAN_ID = APIError(10112, msg='invalid scan_id')
TOO_LARGE_IP_RANGE = APIError(10113, msg='too large ip range')
TOO_LARGE_RESULT_WINDOW = APIError(10114, msg='too large result window')
EMPTY_QUERY = APIError(10115, msg='empty query')
REQUEST_WRONG_URL = APIError(10201, msg='request wrong url')
INTERNAL_ERROR = APIError(50000, msg='server interval error')
SEARCH_TIMEOUT = APIError(50001, msg='search timeout')
