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
        title = (h3.find('a')['href'])
        link = 'https://www.imdb.com' + title
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        date = soup.find('a', {'class': 'ipc-metadata-list-item__list-content-item',
                               'class': 'ipc-metadata-list-item__list-content-item--link',
                               'href': '{title}releaseinfo?ref_=tt_dt_rdat'.format(title=title)}).get_text()
        year = re.search(r"\d{4}", date).group(0)
        return year


def ratings_func(div):
    # global count
    try:
        if (len(div.find_all("div")) == 4):
            return 'No ratings'
        else:
            return div.find("div").attrs.get('data-value')
    except AttributeError:
        return 'No ratings'
        # count += 1


def index_func(i):
    try:
        return {"place": place[i],
                "movie_title": movie_title[i],
                "rating": ratings[i],
                "year": year[i],
                "star_cast": crew[i],
                "about": about[i]
                }
    except IndexError:
        pass


# Downloading imdb bollywood movies from 2000 to 2022
count = 0
movies_list = []
for pages in range(1, 6370, 50):
    print(pages)
    url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,2022-12-31&countries=in&languages=hi&sort=release_date,asc&start={page}&ref_=adv_nxt'.format(
        page=pages)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = soup.select("h3.lister-item-header")
    crew = [" ".join(div.find_all("p")[2].get_text().split()) for div in
            soup.select("div.lister-item.mode-advanced div.lister-item-content")]
    ratings = [ratings_func(div) for div in soup.select("div.lister-item-content")]
    about = ["".join(div.find_all('p', {'class': 'text-muted'})[1].get_text()).split("\n")[1] for div in
             soup.select("div.lister-item-content")]
    place = [h3.find('span', {'class': 'lister-item-index'}).get_text().replace('.', '') for h3 in movies]
    movie_title = [h3.find('a').get_text() for h3 in movies]
    year = [year_func(h3) for h3 in movies]

    # print(len(year))
    # print("Done with page ", pages)
    # print(count)
    # print(year)
    # break
    try:
        temp_list = [index_func(i) for i in range(50)]
        dict_list = [i for i in temp_list if i is not None]
    except IndexError:
        continue

    movies_list.extend(dict_list)

# print(movies_list)
print(len(movies_list))
