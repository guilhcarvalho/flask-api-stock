from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import db

if TYPE_CHECKING:
    from src.models.role import Role


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    role_id: Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role: Mapped[list["Role"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"
