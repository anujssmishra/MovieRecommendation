import requests
from bs4 import BeautifulSoup

url = 'http://www.imdb.com/title/tt0349878/reviews?ref_=tt_urv'
link = 'http://www.imdb.com/title/tt0349878/reviews/_ajax'
res = requests.get(url)

params = {
    'ref_': 'undefined',
    'paginationKey': ''
}

names = []

while True:
    soup = BeautifulSoup(res.text, "html.parser")
    for item in soup.select(".review-container"):
        reviewer_name = item.select_one("span.display-name-link > a").get_text(strip=True)
        # print(reviewer_name)
        review = item.select_one("div.text.show-more__control").get_text(strip=True)
        print(review)
        break
        # names.append(reviewer_name)

    try:
        pagination_key = soup.select_one(".load-more-data[data-key]").get("data-key")
    except AttributeError:
        break
    params['paginationKey'] = pagination_key
    res = requests.get(link, params=params)

print(len(names))
