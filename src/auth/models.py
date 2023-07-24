from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import (
    MetaData,
    Boolean,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    Table,
    Column,
    JSON, func
)

metadata = MetaData()

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permission', JSON),
    Column('created_at', TIMESTAMP, default=func.now()),
    Column('modified_at', TIMESTAMP, default=func.now(), onupdate=func.current_timestamp())
)
