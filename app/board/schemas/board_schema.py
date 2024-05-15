from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class BoardSchema:

    class BoardBase(BaseModel):
        """
        게시판 기본 스키마
        """
        seq: int
        name: str
        # public: Literal["True", "False"]
        public: bool = Field(..., description="(true, 공개), (false, 비공개)")
        created_at: datetime
        updated_at: datetime
        post_cnt: int
        member_seq: int

    class BoardCreate(BaseModel):
        """
        게시판 생성 스키마
        """
        name: str
        # public: Literal[True, False]
        public: bool = Field(..., description="(true, 공개), (false, 비공개)")

        # relationship data 반환여부
        # class Config:
        #     orm_mode = True

    class BoardByOrmMode(BoardBase):
        """
        ORM 모드 적용 게시판 스키마
        """
        # relationship data 반환여부
        class Post(BaseModel):
            seq: int
            title: str
            content: str
            created_at: datetime
            updated_at: datetime

        posts: Optional[List[Post]] = None
        # class Config:
        #     orm_mode = True

    class BoardUpdate(BoardCreate):
        """
        게시판 수정 스키마
        """
        pass
