from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def get_year(h3):
    try:
        return re.findall(r'\d+', h3.find('span', {'class': 'lister-item-year'}).get_text())[0]
    except IndexError:
        title = (h3.find('a')['href'])
        link = 'https://www.imdb.com' + title
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        # noinspection SpellCheckingInspection
        date = soup.find('a', {'class': 'ipc-metadata-list-item__list-content-item',
                               'class': 'ipc-metadata-list-item__list-content-item--link',
                               'href': '{title}releaseinfo?ref_=tt_dt_rdat'.format(title=title)}).get_text()
        year = re.search(r"\d{4}", date).group(0)
        return year


def get_ratings(div):
    try:
        if len(div.find_all("div")) == 4:
            return 'No ratings'
        else:
            return div.find("strong").get_text()
    except AttributeError:
        return 'No ratings'


def get_index(i):
    try:
        if ratings[i] == "No ratings" and reviews[i] == 0:
            raise IndexError
        return {"Place": place[i],
                "Movie Title": movie_title[i],
                "Rating": ratings[i],
                "Year": year[i],
                # "Star_cast": crew[i],
                # "About": about[i],
                "Reviews": reviews[i]
                }
    except IndexError:
        pass


def get_reviews(h3):
    title = (h3.find('a')['href'])
    url = 'https://www.imdb.com' + title + 'reviews?ref_=tt_urv'
    link = 'https://www.imdb.com' + title + 'reviews/_ajax'
    response = requests.get(url)

    params = {
        'ref_': 'undefined',
        'paginationKey': ''
    }

    reviews_total = []

    while True:
        soup = BeautifulSoup(response.text, "html.parser")
        review_count = 0
        for item in soup.select(".review-container"):
            # reviewer_name = item.select_one("span.display-name-link > a").get_text(strip=True)
            # review = item.select_one("div.text.show-more__control").get_text(strip=True)
            # reviews_total.append({"Reviewer name": reviewer_name, "Review": review})
            review_count += 1

        try:
            pagination_key = soup.select_one(".load-more-data[data-key]").get("data-key")
        except AttributeError:
            break
        params['paginationKey'] = pagination_key
        response = requests.get(link, params=params)

    return review_count


def get_about(h3):
    title = (h3.find('a')['href'])
    link = 'https://www.imdb.com' + title + 'plotsummary?ref_=adv_pl'
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.select_one('li.ipl-zebra-list__item > p').get_text(strip=True)


# Downloading imdb bollywood movies from 2000 to 2022
movies_list = []
for pages in range(5001, 6373, 50):
    url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,' \
          '2022-12-31&countries=in&languages=hi&sort=release_date,asc&start={page}&ref_=adv_nxt'.format(page=pages)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    movies = soup.select("h3.lister-item-header")
    crew = [" ".join(div.find_all("p")[2].get_text().split()) for div in
            soup.select("div.lister-item.mode-advanced div.lister-item-content")]
    ratings = [get_ratings(div) for div in soup.select("div.lister-item-content")]
    about = [get_about(h3) for h3 in movies]
    place = [h3.find('span', {'class': 'lister-item-index'}).get_text().replace('.', '') for h3 in movies]
    movie_title = [h3.find('a').get_text() for h3 in movies]
    year = [get_year(h3) for h3 in movies]
    reviews = [get_reviews(h3) for h3 in movies]
    try:
        temp_list = [get_index(i) for i in range(50)]
        dict_list = [i for i in temp_list if i is not None]
    except IndexError:
        continue

    movies_list.extend(dict_list)
    # break
    # print("Done with page", pages)

# print(movies_list)
##.......##
df = pd.DataFrame(movies_list)
df.to_csv('quantitative_part6.csv', index=False)
