import bcrypt
import jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from core.redis.redis_conn import redis_cache
from fastapi import HTTPException
from ..models.member import Member
from ..schemas import MemberToken

JWT_SECRET = "01414aaaf4b7a94e8c5183e038a1717d55d38d45f77881a37777afd6d76ab2e2"
JWT_ALGORITHM = "HS256"


class MemberService:

    def join(self, member: dict, db: Session):
        """회원가입
        :param member:
        :param db:
        :return:
        """
        if not member.get('email') or not member.get('password') or not member.get('fullname'):
            raise HTTPException(status_code=404, detail="join member required params empty")

        check_email_exist = self.is_email_exist(member.get('email'), db)
        if check_email_exist:
            raise HTTPException(status_code=404, detail="already used email")

        hash_pw = bcrypt.hashpw(member.get('password').encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        member['password'] = hash_pw
        member_ = Member(**member)
        db.add(member_)
        db.commit()
        db.refresh(member_)

        # token = dict(msg="성공적으로 회원가입 되었습니다! 환영합니다.",
        #              expire_hours=6,
        #              Authorization=f"Bearer {await create_access_token(member_id=reg_info.member_id, data=MemberToken.from_orm(new_user).dict(), expires_delta=6)}")
        # return Successful(token)
        return member_

    def login(self, member: dict, db: Session):
        """ 로그인
        :param member:
        :param db:
        :return:
        """

        member_ = self.find_by_email(member.get('email'), db)
        if not member.get('email') or not member.get('password'):
            raise HTTPException(status_code=404, detail="아이디 또는 비밀번호가 올바르지 않습니다")
        if not member_:
            raise HTTPException(status_code=404, detail="아이디 또는 비밀번호가 올바르지 않습니다")

        is_verified = bcrypt.checkpw(member.get('password').encode("utf-8"), member_.password.encode("utf-8"))
        if not is_verified:
            raise HTTPException(status_code=404, detail="아이디 또는 비밀번호가 올바르지 않습니다")

        # Members.filter(session, member_id=user_info.member_id).update(auto_commit=True, last_log=D.datetime(),
        # ipaddress=request.state.ip)

        expire_hours = 6
        token = dict(
            msg="로그인 완료",
            expire_hours=expire_hours,
            Authorization=self.create_access_token(member_email=member_.email,
                                                   data=MemberToken.from_orm(member_).dict(),
                                                   expires_delta=expire_hours))
        return token

    @classmethod
    def logout(cls, member: dict):
        """ 로그아웃
        :param member:
        :return:
        """
        redis_cache.delete(member.get('email'))

    @staticmethod
    def create_access_token(member_email: str = None, data: dict = None, expires_delta: int = None):
        """ access_token을 생성합니다.
        :param member_email:
        :param data:
        :param expires_delta:
        :return:
        """
        to_encode = data.copy()
        if expires_delta:
            to_encode.update({"exp": datetime.now() + timedelta(hours=expires_delta)})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Redis 등록
        redis_cache.hset(member_email, encoded_jwt, 'login')
        redis_cache.expire(member_email, expires_delta * 60 * 60)

        return encoded_jwt

    @staticmethod
    def is_email_exist(email, db):
        """ 이메일 존재여부을 확인합니다.
        :param email:
        :param db:
        :return:
        """
        member = db.query(Member).filter(Member.email == email).first()
        if not member:
            return False
        return True

    @staticmethod
    def find_by_email(email, db):
        """ 이메일 기준으로 회원을 조회합니다.
        :param email:
        :param db:
        :return:
        """
        member = db.query(Member).filter(Member.email == email).first()
        return member
