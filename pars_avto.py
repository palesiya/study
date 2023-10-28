import requests
from bs4 import BeautifulSoup as BS


class Parsing:
    def __init__(self, url):
        self._start_url = url
        self._result = []

    def _get_html(self):
        res = requests.get(self._start_url)
        if res.status_code == 200:
            return res.text
        raise ValueError(f"Status_code - {res.status_code}")

    def parse(self):
        sp = self._get_html()
        soup = BS(sp, features="html.parser")
        selector = "main"
        main_box = soup.find(selector)
        items = main_box.find_all("div", class_="listing__items")
        for item in items:
            info = {}
            try:
                info.update(
                    title=item.find("div", class_="listing-item__about").find("a").get_text(strip=True),
                    parameter=item.find("div", class_="listing-item__message").get_text(strip=True),
                    price=item.find("div", class_="listing-item__price").get_text(strip=True)
                )
            except AttributeError:
                ...
            else:
                self._result.append(info)

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self._result[item]
        raise TypeError("Not str")

    def __iter__(self):
        self._cursor = 0
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


if __name__ == '__main__':
    URL = "https://cars.av.by/filter?brands[0][brand]=1238&price_usd[max]=4000&transmission_type=1"
    pars_page = Parsing(URL)
    pars_page.parse()
    for el in pars_page:
        print(el)
