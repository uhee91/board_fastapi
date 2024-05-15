
from sqlalchemy import (
    Column, String, DateTime, func, BigInteger, Text, ForeignKey
)
from sqlalchemy.orm import relationship

from core.db import Base


class Post(Base):
    """
    게시글 모델
    """
    __tablename__ = "posts"

    seq = Column(BigInteger, primary_key=True, autoincrement="auto", )
    title = Column(String(50), unique=True, nullable=False)
    content = Column(Text, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())

    # 자식 객체는 외래키로 부모 객체를 참조한다.
    board_seq = Column(BigInteger, ForeignKey('boards.seq'))
    # 부모 객체를 참조하는 참조 변수
    board = relationship("Board", back_populates="posts")

    member_seq = Column(BigInteger, ForeignKey('members.seq'))
    member = relationship("Member", back_populates="posts")

    # one-to-many 의 참조 변수. uselist 를 False 로 설정하여 하나의 객체만 참조하도록 설정
    # member = relationship("User", back_populates="team", uselist=False)
    # many-to-many:  연관 테이블은 relationship.secondary 속성으로 지정된다.
    # member = relationship("User", back_populates="team", uselist=False, secondary=association_table,)

    @staticmethod
    def update(post_: object, update_dic: dict):
        """ 게시글을 수정하는 함수입니다.
        :param post_:
        :param update_dic:
        :return:
        """
        for key, value in update_dic.items():
            setattr(post_, key, value)
