from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import db

if TYPE_CHECKING:
    from src.models.user import User


class Role(db.Model):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped["User"] = relationship(back_populates="role")

    def __repr__(self):
        return f"Role(id={self.id!r}, name={self.name!r})"
