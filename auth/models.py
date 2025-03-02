from typing import List

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.dafunk import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    package: Mapped[List["Packages"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Packages(Base):
    __tablename__ = "packages"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="package")
    name: Mapped[str] = mapped_column(String(100), index=True, unique=True)
    permissions: Mapped[List["PackagesPermissions"]] = relationship(back_populates="package", cascade="all, delete-orphan")

class PackagesPermissions(Base):
    __tablename__ = "packages_permissions"
    id: Mapped[int] = mapped_column(primary_key=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id"))
    package: Mapped["Packages"] = relationship(back_populates="permissions")
    scope: Mapped[str] = mapped_column(String(50))
    value: Mapped[int] = mapped_column(Integer())