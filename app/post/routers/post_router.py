
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.requests import Request

from core.db import get_db
from ..schemas import PostCreate, PostBase, PostUpdate, PostByOrmMode
from ..services.post_service import PostService
from fastapi_pagination.cursor import CursorPage
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, desc
from ..models import Post
from starlette.exceptions import HTTPException

router = APIRouter()


@router.post("/board/{board_seq}/posts", response_model=PostBase)
def create_post(request: Request, board_seq: int, post: PostCreate, db: Session = Depends(get_db)):
    post_dic = post.dict()
    post_dic.update({"board_seq": board_seq})
    user_dic = request.state.user.dict()
    post = PostService().add_post(user_dic, post_dic, db)
    return post


@router.get("/board/{board_seq}/posts", response_model=CursorPage[PostBase])
def get_posts(request: Request, board_seq: int, db: Session = Depends(get_db)) -> CursorPage[PostBase]:
    user_dic = request.state.user.dict()

    from board.services.board_service import BoardService
    is_board = BoardService().is_board_by_seq(user_dic, board_seq, db)
    if is_board:
        return paginate(db, select(Post).where(Post.board_seq == board_seq).order_by(desc(Post.seq)))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="조회 권한이 없습니다.")


@router.get("/board/{board_seq}/posts/{seq}", response_model=PostByOrmMode)
def get_post(request: Request, board_seq: int, seq: int, db: Session = Depends(get_db)):
    user_dic = request.state.user.dict()
    user_dic.update({"board_seq": board_seq})
    posts = PostService().find_post_by_seq(user_dic, seq, db)
    return posts


@router.put("/board/{board_seq}/posts/{seq}", response_model=PostBase)
def update_post(request: Request, board_seq: int, seq: int, post: PostUpdate, db: Session = Depends(get_db)):
    user_dic = request.state.user.dict()
    user_dic.update({"board_seq": board_seq})
    post = PostService().modify_post(user_dic, seq, post.dict(), db)
    return post


@router.delete("/board/{board_seq}/posts/{seq}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(request: Request, board_seq: int, seq: int, db: Session = Depends(get_db)):
    user_dic = request.state.user.dict()
    user_dic.update({"board_seq": board_seq})
    PostService().delete_post(user_dic, seq, db)
    return {"message": "Post deleted"}
