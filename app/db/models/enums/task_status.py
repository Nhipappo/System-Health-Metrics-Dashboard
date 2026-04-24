from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLITED = "complited"
    FAILED = "failed"

    @property
    def display_name(self) -> str:
        """Человекочитаемое название (методы enum'ов - удобная штука)"""
        names = {
            self.PENDING: "В обработке",
            self.PROCESSING: "В процессе",
            self.COMPLITED: "Завершена",
            self.FAILED: "Провалена"
        }
        return names[self]