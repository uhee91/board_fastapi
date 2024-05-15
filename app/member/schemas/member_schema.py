from datetime import datetime
from pydantic import BaseModel, EmailStr


class MemberSchema:

    class MemberBase(BaseModel):
        """
        회원 기본 스키마
        """
        seq: int
        fullname: str
        email: EmailStr
        password: str
        created_at: datetime
        updated_at: datetime

    class MemberCreate(BaseModel):
        """
        회원 생성 스키마
        """
        fullname: str
        email: EmailStr
        password: str

    class MemberLogin(BaseModel):
        """
        회원 로그인 스키마
        """
        email: EmailStr
        password: str

    class MemberToken(BaseModel):
        """
        회원 토큰 스키마
        """
        seq: int
        fullname: str
        email: EmailStr

        class Config:
            # orm_mode = True
            from_attributes = True

    # class MemberByOrmMode(BoardBase):
    #     # relationship data 반환여부
    #     class Post(BaseModel):
    #         seq: int
    #         title: str
    #         content: str
    #         created_at: datetime
    #         updated_at: datetime
    #
    #     posts: Optional[List[Post]] = None
    #     # class Config:
    #     #     orm_mode = True
    #
    # class MemberUpdate(BoardCreate):
    #     pass