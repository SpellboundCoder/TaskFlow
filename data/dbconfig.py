from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy import String
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
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    websites: Mapped[List["Website"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r}, password={self.password!r})"


class Website(Base):
    __tablename__ = "websites"
    id: Mapped[int] = mapped_column(primary_key=True)
    website: Mapped[str] = mapped_column(String(50))
    icon: Mapped[str] = mapped_column(String(60))
    tag: Mapped[str] = mapped_column(String(60))
    email: Mapped[str] = mapped_column(String(120))
    username: Mapped[str] = mapped_column(String(120), nullable=True)
    mobile: Mapped[str] = mapped_column(String(120), nullable=True)
    password: Mapped[str] = mapped_column(String(120))
    date: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="websites")

    def __repr__(self) -> str:
        return f"Website(id={self.id!r}, website={self.website!r}, email={self.email!r}, password={self.password})"


Base.metadata.create_all(engine)

