from sqlalchemy.orm import Session

from ..models import Board
from fastapi import HTTPException
from operator import sub, add

from sqlalchemy import or_, exists, and_


class BoardService:

    @classmethod
    def add_board(cls, board: dict, db: Session):
        """ 게시판을 등록합니다.
        :param board:
        :param db:
        :return:
        """
        board = Board(**board)
        db.add(board)
        db.commit()
        db.refresh(board)
        return board

    def modify_board(self, user_dic: dict, seq: int, board: dict, db: Session):
        """ 게시판을 수정합니다.
        :param user_dic:
        :param seq:
        :param board:
        :param db:
        :return:
        """
        if not board.get('name'):
            raise HTTPException(status_code=404, detail="Board Name is not Valid")

        board_ = self.find_board_by_seq_to_member_seq(user_dic, seq, db)
        if board_ is None:
            raise HTTPException(status_code=404, detail="Board not found")

        # synchronize_session : 메모리에 있는 객체를 동기화하지 않는다.
        # board_.update(board, synchronize_session=False)
        Board.update(board_, board)
        db.commit()

        return board_

    @classmethod
    def find_board_by_seq(cls, user_dic: dict, seq: int, db: Session):
        """게시판 일련번호 기준으로 게시판을 조회합니다.
        :param user_dic:
        :param seq:
        :param db:
        :return:
        """
        board = db.query(Board).where(Board.seq == seq).where(
            or_(Board.member_seq == user_dic['seq'], Board.public == True)).first()

        if board is None:
            raise HTTPException(status_code=404, detail="권한이 없습니다.")
        return board

    def delete_board(self, user_dic: dict, seq: int, db: Session):
        """ 게시판을 삭제합니다.
        :param user_dic:
        :param seq:
        :param db:
        :return:
        """
        board_ = self.find_board_by_seq_to_member_seq(user_dic, seq, db)
        if board_ is None:
            raise HTTPException(status_code=404, detail="권한이 없습니다.")

        db.delete(board_)
        db.commit()

    def modify_post_cnt_by_seq(self, user_dic: dict, seq: int, db: Session, is_delete: bool = False):
        """게시판 일련번호 기준으로 게시글 수를 수정합니다.
        :param user_dic:
        :param seq:
        :param db:
        :param is_delete:
        :return:
        """
        board_ = self.find_board_by_seq_to_member_seq(user_dic, seq, db)
        if board_ is None:
            raise HTTPException(status_code=404, detail="Board not found")

        op = sub if is_delete else add
        board_.post_cnt = op(board_.post_cnt, 1)
        if board_.post_cnt < 0:
            board_.post_cnt = 0

    @classmethod
    def find_board_by_seq_to_member_seq(cls, user_dic, seq, db):
        """ 게시판 일련번호, 회원 일련번호 기준으로 게시판을 조회합니다.
        :param user_dic:
        :param seq:
        :param db:
        :return:
        """
        db_ = db.query(Board).where(Board.seq == seq)
        if user_dic.get("seq"):
            db_ = db_.where(Board.member_seq == user_dic['seq'])
        board_ = db_.first()

        return board_

    @classmethod
    def is_board_by_seq(cls, user_dic, seq, db):
        """게시판 조회 검증합니다.
        :param user_dic:
        :param seq:
        :param db:
        :return:
        """

        is_board_ = db.query(exists()
                             .where(or_(and_(Board.seq == seq, Board.public == True),
                                    and_(Board.member_seq == user_dic["seq"],
                                     Board.seq == seq,
                                     Board.public == False)))).scalar()
        if is_board_:
            return True
        return False
    