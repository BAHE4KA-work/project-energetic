from typing import List
from sqlalchemy import Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db.base import Base


class RawData(Base):
    __tablename__ = 'raw_datum'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    accountId: Mapped[int] = mapped_column(Integer)
    isCommercial: Mapped[bool] = mapped_column(Boolean)
    address: Mapped[str] = mapped_column(String)
    buildingType: Mapped[str] = mapped_column(String)
    roomsCount: Mapped[int] = mapped_column(Integer, nullable=True)
    residents_count: Mapped[int] = mapped_column(Integer, nullable=True)
    totalArea: Mapped[float] = mapped_column(Float, nullable=True)
    consumption: Mapped[str] = mapped_column(String) # Список через запятую пробел


class AddressCard(Base):
    __tablename__ = 'address_cards'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String, unique=True)

    avg_cons: Mapped[float] = mapped_column(Float) # В среднем по месяцам
    level: Mapped[int] = mapped_column(Integer, nullable=True)
    deviation: Mapped[str] = mapped_column(String) # Отклонение от нормы в коэф.
    times_checked: Mapped[int] = mapped_column(Integer)
    filling_coef: Mapped[float] = mapped_column(Float)
    potential_losses: Mapped[float] = mapped_column(Float) # Рублей (по разнице с эталоном)
    building_type: Mapped[str] = mapped_column(String)

    events: Mapped[List["Event"]] = relationship(
        "Event",
        back_populates="address_card",
        cascade="all, delete-orphan",
    )


class Master(Base):
    __tablename__ = 'masters'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)  # Код для авторизации

    events: Mapped[list["Event"]] = relationship("Event", back_populates="worker")


class Event(Base):
    __tablename__ = 'events'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    address_card_id: Mapped[int] = mapped_column(ForeignKey("address_cards.id"), nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False)  # этапы проверки
    is_done: Mapped[bool] = mapped_column(Boolean, default=False)
    worker_id: Mapped[int | None] = mapped_column(ForeignKey("masters.id"), nullable=True)

    address_card: Mapped['AddressCard'] = relationship('AddressCard', back_populates='events')
    worker: Mapped["Master"] = relationship("Master", back_populates="events")
