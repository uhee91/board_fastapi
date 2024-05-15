# Reach schema directly through a variable
from .post_schema import PostSchema

PostBase = PostSchema.PostBase
PostCreate = PostSchema.PostCreate
PostUpdate = PostSchema.PostUpdate
PostByOrmMode = PostSchema.PostByOrmMode
