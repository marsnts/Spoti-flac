from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def download(self, song):
        pass

    @property
    @abstractmethod
    def name(self):
        pass