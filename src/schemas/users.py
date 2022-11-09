from pydantic import BaseModel, Field, PositiveInt


class UserCreateSchema(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=10
    )
    password: str = Field(
        max_length=8
    )


class UserUpdateSchema(BaseModel):
    username: str
    password: str | None
    active: bool | None
    admin: bool | None


class UserResponseSchema(BaseModel):
    user_id: PositiveInt
    username: str
    active: bool
    admin: bool
