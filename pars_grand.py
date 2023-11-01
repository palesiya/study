from base_class import BaseParser
from bs4 import BeautifulSoup as BS


class Parsing(BaseParser):
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


if __name__ == '__main__':
    URL = "https://autogrand.by/cars/?price-to=7000"
    HOST = "https://autogrand.by/"
    pars_page = Parsing(URL)
    pars_page.parse()
    #print(pars_page[0::])
    for el in pars_page:
        print(el)
