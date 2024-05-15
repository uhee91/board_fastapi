from ..schemas import BoardCreate, BoardBase, BoardUpdate
from ..services.board_service import BoardService
from ..models import Board
from starlette import status
from starlette.requests import Request
from core.db import get_db
from fastapi import Depends, APIRouter
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, or_

router = APIRouter()


@router.post("/boards", response_model=BoardBase)
def create_board(request: Request, board: BoardCreate, db: Session = Depends(get_db)):
    board_dic = board.dict()
    board_dic.update({"member_seq": request.state.user.seq})
    board = BoardService().add_board(board_dic, db)
    return board


@router.get("/boards", response_model=CursorPage[BoardBase])
def get_boards(request: Request, db: Session = Depends(get_db)) -> CursorPage[BoardBase]:
    member_seq = request.state.user.seq
    return paginate(db, select(Board).where(or_(Board.public == True, Board.member_seq == member_seq)).order_by(desc(Board.post_cnt)))


@router.get("/boards/{seq}", response_model=BoardBase)
def get_board(request: Request, seq: int, db: Session = Depends(get_db)):
    user_dic = request.state.user.dict()
    board = BoardService().find_board_by_seq(user_dic, seq, db)
    return board


@router.put("/boards/{seq}", response_model=BoardBase)
def update_board(request: Request, seq: int, board: BoardUpdate, db: Session = Depends(get_db)):
    user_dic = request.state.user.dict()
    board = BoardService().modify_board(user_dic, seq, board.dict(), db)
    return board


@router.delete("/boards/{seq}", status_code=status.HTTP_204_NO_CONTENT)
def delete_board(request: Request, seq: int, db: Session = Depends(get_db)):
    user_dic = request.state.user.dict()
    BoardService().delete_board(user_dic, seq, db)
    return {"message": "Board deleted"}
