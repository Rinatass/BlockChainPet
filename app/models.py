from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text
from flask_login import UserMixin
from pydantic import BaseModel, Field, PositiveInt, PositiveFloat
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base, UserMixin):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(40))
    password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(128))

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"


class Transaction(BaseModel):
    creditor: str
    debtor: str
    amount: PositiveFloat

    def get_hashable(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return f"  Creditor={self.creditor}\n  Debtor={self.debtor}\n  Amount={self.amount}"


class Block(BaseModel):
    id: int
    transaction: dict
    previous_block_hash: str
    proof: int
    hash: str

    def get_hashable(self):
        return str(self.__dict__)

    def __repr__(self):
        return f"Id={self.id}\nTransaction\n" \
               f"{self.transaction}Previous block hash={self.previous_block_hash}\nProof={self.proof}"

    def __str__(self):
        return f"Id={self.id}\nHash= {self.hash}\nTransaction\n" \
               f"{self.transaction}\nPrevious block hash={self.previous_block_hash}\nProof={self.proof}"


class BlockChain(BaseModel):
    blocks: List[Block]
