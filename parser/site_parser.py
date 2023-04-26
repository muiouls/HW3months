import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = "https://animego.org/anime/season/2023/spring"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15"
}


def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all("div", class_="animes-list-item media")
    anime = []
    for item in items:
        anime.append({
            "title": item.find("div", class_="h5 font-weight-normal mb-1").find("a").getText(),
            "url": item.find("div", class_="h5 font-weight-normal mb-1").find("a").get("href"),
            "type": item.find("a", class_="text-link-gray text-underline").string,
            "description": item.find("div", class_="description d-none d-sm-block").getText(),
        })
    return anime


def parser():
    html = get_html(URL)
    if html.status_code != 200:
        raise Exception("Error in parser!")
    data = get_data(html.text)
    return data



