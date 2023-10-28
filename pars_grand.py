import requests
from bs4 import BeautifulSoup as BS


URL = "https://autogrand.by/cars/?price-to=7000"
HOST = "https://autogrand.by/"


def get_html(url):
    result = requests.get(url)
    if result.status_code == 200:
        return result
    raise ValueError(f"Status_code - {result.status_code}")


def parse(html):
    soup = BS(html, "html.parser")
    items = soup.find_all("div", class_="vehica-inventory-v1__results")
    res = []

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
            res.append(info)

    return res


html = get_html(URL)
print(parse(html.text))


