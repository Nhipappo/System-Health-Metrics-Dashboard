from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

    @property
    def display_name(self) -> str:
        """Человекочитаемое название (методы enum'ов - удобная штука)"""
        names = {
            self.PENDING: "В обработке",
            self.PROCESSING: "В процессе",
            self.COMPLETED: "Завершена",
            self.FAILED: "Провалена",
        }
        return names[self]
