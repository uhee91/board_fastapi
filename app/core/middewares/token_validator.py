import datetime
import time
import re

import jwt

from jwt.exceptions import ExpiredSignatureError, DecodeError
from starlette.requests import Request
from starlette.responses import JSONResponse

from member.schemas import MemberToken
from core.redis.redis_conn import redis_cache


from member.services.member_service import JWT_SECRET, JWT_ALGORITHM


async def access_control(request: Request, call_next):
    print(" === start access_control ===")
    request.state.req_time = datetime.datetime.now()
    request.state.start = time.time()
    request.state.inspect = None
    request.state.user = None
    request.state.service = None

    ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
    request.state.ip = ip.split(",")[0] if "," in ip else ip
    headers = request.headers
    cookies = request.cookies

    url = request.url.path

    if "authorization" in headers.keys():
        jwt_token, token_info = await token_decode_without_error(access_token=headers.get("Authorization"))
        if token_info:
            request.state.user = MemberToken(**token_info)
            request.state.jwt_token = jwt_token

    # if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
    #     response = await call_next(request)
    #     if url != "/":
    #         await api_logger(request=request, response=response)
    #     return responses

    try:
        if url.startswith("/board") or url.startswith("/boards") or url.startswith("/members"):
            # api 인경우 헤더로 토큰 검사
            if "authorization" in headers.keys():
                print(headers.get("Authorization"))
                jwt_token, token_info = await token_decode(access_token=headers.get("Authorization"))
                request.state.user = MemberToken(**token_info)
                request.state.jwt_token = jwt_token
                # 토큰 없음
            else:
                print(" === done ===")
                if "Authorization" not in headers.keys():
                    raise Exception("No authorization header")

        response = await call_next(request)
        # await api_logger(request=request, response=response)
    except Exception as e:
        print(str(e))
        # error = exception_handler(e)
        error_dict = dict(status=404, msg=str(e), detail=str(e), code=404)
        response = JSONResponse(status_code=404, content=error_dict)
        # await api_logger(request=request, error=error)
    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False


async def token_validate_redis(email, access_token):

    data = redis_cache.hget(email, access_token)
    print(" ==== token validate ====")
    print(data)
    print(" ==== token validate ====")
    if data is None:
        raise Exception("Token does not exists")


async def token_decode(access_token):
    """
    :param access_token:
    :return:
    """
    try:
        access_token = access_token.replace("Bearer ", "")
        print(access_token)
        payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(payload)
        await token_validate_redis(payload['email'], access_token)
    except ExpiredSignatureError:
        raise Exception("Token expired")
    except DecodeError:
        raise Exception("Invalid token")
    return access_token, payload

async def token_decode_without_error(access_token):
    """
    :param access_token:
    :return:
    """
    payload = None
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        token_validate_redis(payload['member_id'], access_token)
    except Exception as e:
        pass
    return access_token, payload


# async def exception_handler(error: Exception):
#     print(error)
#     if isinstance(error, sqlalchemy.exc.OperationalError):
#         error = SqlFailureEx(ex=error)
#     if not isinstance(error, APIException):
#         error = APIException(ex=error, detail=str(error))
#     return error
