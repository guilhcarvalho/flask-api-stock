from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.models import db


class Dji_Part(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    dji_part_number: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(sa.String, unique=False, nullable=False)
    quantity: Mapped[int] = mapped_column(sa.Integer, unique=False, nullable=False)
    last_update: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self):
        return f"DJI Part(id={self.id!r}, DJI Part Number={self.dji_part_number!r}, Last Update={self.last_update!r}, Author ID={self.author_id!r})"
