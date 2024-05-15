from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from ..schemas import MemberCreate, MemberLogin
from ..services.member_service import MemberService
from starlette.requests import Request

router = APIRouter()


@router.post("/signup", status_code=200)
def join_member(member: MemberCreate, db: Session = Depends(get_db)):
    member = MemberService().join(member.dict(), db)
    return {"message": "가입 성공"}


@router.post("/login", status_code=200)
def login(member: MemberLogin, db: Session = Depends(get_db)):
    token = MemberService().login(member.dict(), db)
    return token


@router.post("/members/logout", status_code=200)
def logout(request: Request):
    MemberService().logout(request.state.user.dict())
    return {"message": "logged out"}
