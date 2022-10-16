from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def year_func(h3):
    global count
    try:
        return re.findall(r'\d+', h3.find('span', {'class': 'lister-item-year'}).get_text())[0]
    except IndexError:
        count += 1


# Downloading imdb bollywood movies from 2000 to 2022
count = 0
movies_list = []
for pages in range(6351, 6370, 50):
    url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2022-12-31&countries=in&languages=hi&sort=release_date,asc&start={page}&ref_=adv_nxt'.format(
        page=pages)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = soup.select("h3.lister-item-header")
    crew = [" ".join(div.find_all("p")[2].get_text().split()) for div in
            soup.select("div.lister-item.mode-advanced div.lister-item-content")]
    ratings = ['No ratings' if (len(div.find_all("div")) == 3) else div.find("div").attrs.get('data-value')
               for div in soup.select("div.ratings-bar")]
    about = ["".join(div.find_all('p', {'class': 'text-muted'})[1].get_text()).split("\n")[1] for div in
             soup.select("div.lister-item-content")]
    place = [h3.find('span', {'class': 'lister-item-index'}).get_text().replace('.', '') for h3 in movies]
    movie_title = [h3.find('a').get_text() for h3 in movies]
    # year = [re.findall(r'\d+', h3.find('span', {'class': 'lister-item-year'}).get_text())[0] if (
    # len(h3.find('span', {'class': 'lister-item-year'}).get_text()) > 0) else '2012' for h3 in movies]
    year = [year_func(h3) for h3 in movies]
    print(len(place))
    dict_list = [{"place": place[i],
                  "movie_title": movie_title[i],
                  "rating": ratings[i],
                  "year": year[i],
                  "star_cast": crew[i],
                  "about": about[i]
                  } for i in range(50)]

    movies_list.extend(dict_list)
    print("Done with page ", pages)
    print(count)

# print(movies_list)
print(len(movies_list))
