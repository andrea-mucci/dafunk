import uuid
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import HSTORE
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.dafunk import Base

class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(125), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    is_admin: Mapped[bool] = mapped_column(default=False)
    apikey: Mapped[List["APIKey"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class APIKey(Base):
    __tablename__ = "apikey"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    permissions: Mapped[HSTORE] = mapped_column(MutableDict.as_mutable(HSTORE))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="apikey")
