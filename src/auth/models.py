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

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False),
    Column('email', String, nullable=False),
    Column('first_name', String, nullable=True),
    Column('last_name', String, nullable=True),
    Column('middle_name', String, nullable=True),
    Column('is_active', String, default=False, nullable=False),
    Column('is_verified', String, default=False, nullable=False),
    Column('is_superuser', String, default=False, nullable=False),
    Column('created_at', TIMESTAMP, default=func.now()),
    Column('modified_at', TIMESTAMP, default=func.now(), onupdate=func.current_timestamp()),
    Column('role_id', Integer, ForeignKey(role.c.id))
)
