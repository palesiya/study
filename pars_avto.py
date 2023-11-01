from base_class import BaseParser
from bs4 import BeautifulSoup as BS


class Parsing(BaseParser):
    def parse(self):
        sp = self._get_html()
        soup = BS(sp, features="html.parser")
        selector = "main"
        main_box = soup.find(selector)
        items = main_box.find_all("div", class_="listing-item")
        for item in items:
            info = {}
            try:
                info.update(
                    title=item.find("div", class_="listing-item__about").find("a").get_text(strip=True),
                    price=(
                        item.find("div", class_="listing-item__price")
                        .get_text(strip=True)
                        .replace("&nbsp;", "")
                        .replace("\u2009", " ")
                        .replace("\xa0", " ")),
                    parameter=item.find("div", class_="listing-item__message").get_text(strip=True)
                )
            except AttributeError:
                ...
            else:
                self._result.append(info)


if __name__ == '__main__':
    URL = "https://cars.av.by/filter?brands[0][brand]=1238&price_usd[max]=4000&transmission_type=1&page=2"
    pars_page = Parsing(URL)
    pars_page.parse()
    #print(pars_page[0::])
    for el in pars_page[0::]:
        print(el)
