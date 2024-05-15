from sqlalchemy import (
    Column, String, DateTime, func, BigInteger, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship

from core.db import Base

from post.models.post import Post


class Board(Base):
    """
    게시판 모델
    """
    __tablename__ = "boards"

    seq = Column(BigInteger, primary_key=True, autoincrement="auto", )
    name = Column(String(50), unique=True, nullable=False)
    public = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    post_cnt = Column(BigInteger, default=0, nullable=False)

    member_seq = Column(BigInteger, ForeignKey('members.seq'))
    member = relationship("Member", back_populates="boards")

    posts = relationship("Post", order_by=Post.seq, back_populates="board", cascade="all, delete-orphan")

    @staticmethod
    def update(board_: object, update_dic: dict):
        """ 게시판 수정하는 함수입니다.
        :param board_:
        :param update_dic:
        :return:
        """
        for key, value in update_dic.items():
            setattr(board_, key, value)

