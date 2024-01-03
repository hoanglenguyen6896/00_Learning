import bs4
import requests

base_url = 'http://quotes.toscrape.com/page/{}'


author_set = set()
page = 1
while True:
    page_url = base_url.format(page)
    res = requests.get(page_url.format(1))

    if "No quotes found!" in res.text:
        break

    soup = bs4.BeautifulSoup(res.text, 'lxml')

    # Print author
    author_soup = soup.select(".author")
    for author_name in author_soup:
        author_set.add(author_name.text)
    page += 1



print(author_set)


