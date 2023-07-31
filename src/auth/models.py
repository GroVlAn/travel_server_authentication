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

Role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permission', JSON),
    Column('created_at', TIMESTAMP, default=func.now()),
    Column('modified_at', TIMESTAMP, default=func.now(), onupdate=func.current_timestamp())
)

User = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=False, unique=True),
    Column('email', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('first_name', String, nullable=True),
    Column('last_name', String, nullable=True),
    Column('middle_name', String, nullable=True),
    Column('is_active', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('created_at', TIMESTAMP, default=func.now()),
    Column('modified_at', TIMESTAMP, default=func.now(), onupdate=func.current_timestamp()),
    Column('role_id', Integer, ForeignKey(Role.c.id))
)
