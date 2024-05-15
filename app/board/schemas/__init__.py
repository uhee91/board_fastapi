# Reach schema directly through a variable
from .board_schema import BoardSchema

BoardBase = BoardSchema.BoardBase
BoardCreate = BoardSchema.BoardCreate
BoardUpdate = BoardSchema.BoardUpdate
BoardByOrmMode = BoardSchema.BoardByOrmMode
