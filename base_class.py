from  abc import ABC, abstractmethod
import requests


class BaseParser(ABC):
    def __init__(self, url):
        self._start_url = url
        self._result = []

    def _get_html(self):
        res = requests.get(self._start_url)
        if res.status_code == 200:
            return res.text
        raise ValueError(f"Status_code - {res.status_code}")

    @abstractmethod
    def parse(self):
        pass

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self._result[item]
        raise TypeError("Not str")

    def __iter__(self):
        self._cursor = -1
        if not self._result:
            self.parse()
        return self

    def __next__(self):
        self._cursor += 1
        try:
            return self._result[self._cursor]
        except IndexError:
            del self._cursor
            raise StopIteration()
