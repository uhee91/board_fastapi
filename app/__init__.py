
import sys
from pathlib import Path

# 현재 스크립트의 디렉토리를 가져옴
script_directory = Path(__file__).resolve().parent
# 모듈이 위치한 디렉토리를 sys.path에 추가
sys.path.append(str(script_directory))

# from .board.models import *
# from .post.models import *
from .member.models import *
# from .board.routers import *
# from .core import *