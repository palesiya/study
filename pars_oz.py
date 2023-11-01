from bs4 import BeautifulSoup as BS
from base_class import BaseParser


class Parsing(BaseParser):
    def parse(self):
        sp = self._get_html()
        soup = BS(sp, features="html.parser")
        items = soup.find_all("div", class_="products__item item product-card")
        for item in items:
            info = {}
            try:
                info.update(
                    title=item.find("div", class_="product-card__title").get_text(strip=True),
                    rating=item.find("div", class_="product-card__rating").get_text(strip=True),
                    price=(
                        item.find("div", class_="product-card__cost")
                        .find("strong")
                        .get_text(strip=True)
                        .replace("&nbsp;", "")
                        .replace("\xa0", " "))
                )
            except AttributeError:
                ...
            else:
                self._result.append(info)


if __name__ == '__main__':
    URL = "https://oz.by/badges/"
    pars_page = Parsing(URL)
    pars_page.parse()
    #print(pars_page[0::])
    for el in pars_page:
        print(el)
