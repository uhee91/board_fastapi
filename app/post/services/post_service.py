from sqlalchemy.orm import Session

from ..models import Post
from fastapi import HTTPException
from starlette import status


class PostService:

    def add_post(self, user_dic, post_dic: dict, db: Session):
        """ 게시글을 등록합니다.
        :param user_dic:
        :param post_dic:
        :param db:
        :return:
        """
        from board.services.board_service import BoardService

        # 조회가능한 게시판만 등록 가능하게 검증
        is_board = BoardService.is_board_by_seq(user_dic, post_dic.get('board_seq'), db)
        if is_board is None:
            raise HTTPException(status_code=404, detail="Board not found")
        post_ = Post(**post_dic)
        post_.member_seq = user_dic.pop('seq')
        db.add(post_)

        # 트리거 처리?
        BoardService().modify_post_cnt_by_seq(user_dic, post_dic.get('board_seq'), db, False)
        db.commit()
        db.refresh(post_)
        return post_

    @classmethod
    def find_post_by_seq(cls, user_dic: dict, seq: int, db: Session):
        """게시글 일련번호 기준으로 게시글을 조회합니다.
        :param user_dic:
        :param seq:
        :param db:
        :return:
        """
        from board.services.board_service import BoardService
        is_board = BoardService().is_board_by_seq(user_dic, user_dic['board_seq'], db)
        if not is_board:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="권한이 없습니다.")

        post = db.query(Post).where(Post.seq == seq).first()
        if post is None:
            raise HTTPException(status_code=404, detail="Not Post found")

        return post

    def modify_post(self, user_dic: dict, seq: int, post: dict, db: Session):
        """ 게시글을 수정합니다.
        :param user_dic:
        :param seq:
        :param post:
        :param db:
        :return:
        """
        if not post.get('title'):
            raise HTTPException(status_code=404, detail="Post title is not Valid")
        if not post.get('content'):
            raise HTTPException(status_code=404, detail="Post context is not Valid")

        post_ = self.find_post_by_seq(user_dic, seq, db)
        if post_.member_seq != user_dic['seq']:
            raise HTTPException(status_code=404, detail="권한이 없습니다.")

        # synchronize_session : 메모리에 있는 객체를 동기화하지 않는다.
        # post_.update(post, synchronize_session=False)
        Post.update(post_, post)
        db.commit()

        return post_

    def delete_post(self, user_dic: dict, seq: int, db: Session):
        """ 게시글을 삭제합니다.
        :param user_dic:
        :param seq:
        :param db:
        :return:
        """

        post_ = self.find_post_by_seq(user_dic, seq, db)
        if post_.member_seq != user_dic.pop('seq'):
            raise HTTPException(status_code=404, detail="권한이 없습니다.")
        db.delete(post_)

        from board.services.board_service import BoardService
        BoardService().modify_post_cnt_by_seq(user_dic, post_.board_seq, db, True)
        db.commit()
