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
        items = soup.find_all("div", class_="vehica-car-card__inner")
        for item in items:
            info = {}
            try:
                info.update(
                    title=item.find("div", class_="vehica-car-card__content").find("a").get("title"),
                    price=item.find("div", class_="vehica-car-card__price").get_text(strip=True),
                    years=item.find("div", class_="vehica-car-card__info__single").get_text(strip=True),
                    foto=HOST + item.find("div", class_="vehica-car-card__image-bg").find("img").get("src")
                )
            except AttributeError:
                print(item)
            else:
                self._result.append(info)

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


if __name__ == '__main__':
    URL = "https://autogrand.by/cars/?price-to=7000"
    HOST = "https://autogrand.by/"
    pars_page = Parsing(URL)
    pars_page.parse()
    #print(pars_page[0::])
    for el in pars_page:
        print(el)





