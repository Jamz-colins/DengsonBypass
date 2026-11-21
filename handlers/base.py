from abc import ABC, abstractmethod
import requests


class BaseHandler(ABC):
    def __init__(self, session: requests.Session):
        self.session = session

    @abstractmethod
    def resolve(self, url: str) -> str:
        """Menerima short URL dan mengembalikan URL tujuan akhir."""
        pass
