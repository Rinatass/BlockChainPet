from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(40))
    password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(128))

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
