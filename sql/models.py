from sqlalchemy import String, Integer
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            DeclarativeBase)


class Base(DeclarativeBase):
    pass


class GeoFilter(Base):
    __tablename__ = "geo_filter"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    filter: Mapped[str] = mapped_column(String(250), nullable=False)


class ProjectFilter(Base):
    __tablename__ = "project_filter"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    filter: Mapped[str] = mapped_column(String(250), nullable=False)


class BuyerFilter(Base):
    __tablename__ = "buyer_filter"

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    filter: Mapped[str] = mapped_column(String(250), nullable=False)
