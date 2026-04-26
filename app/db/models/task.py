import uuid
from typing import Any, Dict, Optional

from sqlalchemy import JSON, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.models.base import Base
from app.db.models.enums.task_status import TaskStatus
from app.db.models.time_stamped_mixin import TimeStampedMixin


class Task(Base, TimeStampedMixin):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    status: Mapped[TaskStatus] = mapped_column(
        String(20), default=TaskStatus.PENDING, nullable=False, doc="Статус запроса"
    )

    payload: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON, default=dict, nullable=True, doc="Запрос"
    )

    attempts: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, doc="Количество попыток"
    )

    result: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON, nullable=True, doc="Результат операции в формате JSON (успех) или null"
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, doc="Текст ошибки (при неудаче) или null"
    )
