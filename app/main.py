from typing import Annotated

from fastapi import FastAPI, Depends
import uvicorn
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader

from fastapi_pagination import add_pagination
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from board.routers.board_router import router as board_router
from core.middewares.token_validator import access_control
from core.redis.redis_conn import redis_cache
from post.routers.post_router import router as post_router
from member.routers.member_router import router as member_router

app = FastAPI()

# 레디스 초기화
redis_cache.init_cache()

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
# 미들웨어 설정
app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)

# 라우터 설정
app.include_router(board_router, tags=["borad"], dependencies=[Depends(API_KEY_HEADER)])
app.include_router(post_router, tags=["post"], dependencies=[Depends(API_KEY_HEADER)])
app.include_router(member_router, tags=["member"], dependencies=[Depends(API_KEY_HEADER)])
add_pagination(app)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True)