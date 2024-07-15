from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

db_url = "sqlite:///data/database.db"

engine = create_engine(db_url)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"  # noqa
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    tasks: Mapped[List["Task"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.first_name!r}, email={self.email!r}, password={self.last_name!r})"


class Task(Base):
    __tablename__ = "tasks"  # noqa
    id: Mapped[int] = mapped_column(primary_key=True)
    task: Mapped[str] = mapped_column(String(500))
    tag: Mapped[str] = mapped_column(String(60))
    date: Mapped[str] = mapped_column(String(50))
    completed: Mapped[bool] = mapped_column(Boolean())
    deleted: Mapped[bool] = mapped_column(Boolean())
    active: Mapped[bool] = mapped_column(Boolean())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="tasks")

    def __repr__(self) -> str:
        return f"Website(id={self.id!r}, website={self.task!r}, email={self.tag!r}, password={self.date})"


Base.metadata.create_all(engine)
