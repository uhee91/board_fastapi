from datetime import datetime
from pydantic import BaseModel


class PostSchema:

    class PostBase(BaseModel):
        """
        게시글 기본 스키마
        """
        seq: int
        title: str
        content: str
        created_at: datetime
        updated_at: datetime
        board_seq: int

    class PostCreate(BaseModel):
        """
        게시글 생성 스키마
        """
        title: str
        content: str

    class PostByOrmMode(PostBase):
        """
        ORM 모드 적용 게시글 스키마
        """
        pass
        # relationship data 반환여부
        # class Config:
        #     orm_mode = True

    class PostUpdate(BaseModel):
        """
        게시글 수정 스키마
        """
        title: str
        content: str
