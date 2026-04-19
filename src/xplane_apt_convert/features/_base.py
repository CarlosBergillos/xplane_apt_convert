from abc import ABC, abstractmethod


class AptFeature(ABC):
    @staticmethod
    @abstractmethod
    def _schema() -> dict:
        pass

    @abstractmethod
    def _to_record(self) -> dict:
        pass
