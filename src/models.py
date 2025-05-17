from datetime import datetime
from enum import Enum
from typing import List

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String, Numeric, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Server(str, Enum):
    HARMONY = "Harmony"
    MELODY = "Melody"
    CADENCE = "Cadence"


class TradeType(str, Enum):
    WTS = "WTS"
    WTB = "WTB"
    WTT = "WTT"
    PC = "PC"


class Rarity(str, Enum):
    COMMON = "common"
    RARE = "rare"
    SUPREME = "supreme"
    FANTASTIC = "fantastic"


class Currency(str, Enum):
    IRON = "iron"
    COPPER = "copper"
    SILVER = "silver"
    GOLD = "gold"


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    server: Mapped[Server] = mapped_column(SQLEnum(Server))
    player_name: Mapped[str] = mapped_column(String(100))
    trade_type: Mapped[TradeType] = mapped_column(SQLEnum(TradeType))
    message: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    items: Mapped[List["Item"]] = relationship(back_populates="trade")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    trade_id: Mapped[int] = mapped_column(ForeignKey("trades.id"))
    name: Mapped[str] = mapped_column(String(200))
    rarity: Mapped[Rarity] = mapped_column(SQLEnum(Rarity))
    quality_level: Mapped[float] = mapped_column(Numeric(10, 4))
    weight: Mapped[float] = mapped_column(Numeric(10, 4))
    damage: Mapped[float] = mapped_column(Numeric(10, 4))
    price_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)
    price_currency: Mapped[Currency] = mapped_column(SQLEnum(Currency), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    trade: Mapped["Trade"] = relationship(back_populates="items")
    attributes: Mapped[List["ItemAttribute"]] = relationship(back_populates="item")
    traits: Mapped[List["ItemTrait"]] = relationship(back_populates="item")


class ItemAttribute(Base):
    __tablename__ = "item_attributes"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    attribute_name: Mapped[str] = mapped_column(String(50))
    attribute_value: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    item: Mapped["Item"] = relationship(back_populates="attributes")


class ItemTrait(Base):
    __tablename__ = "item_traits"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    trait_type: Mapped[str] = mapped_column(String(50))
    trait_value: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    item: Mapped["Item"] = relationship(back_populates="traits") 