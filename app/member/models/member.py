from sqlalchemy import (
    Column, String, DateTime, func, BigInteger
)
from sqlalchemy.orm import relationship

from core.db import Base

from post.models.post import Post
from board.models.board import Board


class Member(Base):
    """
    회원 모델
    """
    __tablename__ = "members"

    seq = Column(BigInteger, primary_key=True, autoincrement="auto", )
    fullname = Column(String(50), default=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())

    boards = relationship("Board", order_by=Board.seq, back_populates="member", cascade="all, delete-orphan")
    posts = relationship("Post", order_by=Post.seq, back_populates="member", cascade="all, delete-orphan")

    @staticmethod
    def update(member: object, update_dic: dict):
        """ 회원 정보를 수정 합니다.
        :param member:
        :param update_dic:
        :return:
        """
        for key, value in update_dic.items():
            setattr(member, key, value)

