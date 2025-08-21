# STDLIB
import enum
import uuid

# THIRDPARTY
from sqlalchemy import ForeignKey, Text, text
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

# FIRSTPARTY
from app.database import Base


class StatusEnum(enum.Enum):
    CREATED = "CREATED"
    WORKING = "WORKING"
    COMPLETED = "COMPLETED"


class Tasks(Base):
    __tablename__ = "tasks"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.uuid"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(
        Text, nullable=True
    )  # я посчитал, что описания задачи может и не быть, если так захочет пользователь
    status: Mapped[StatusEnum] = mapped_column(
        postgresql.ENUM(StatusEnum), nullable=False
    )
