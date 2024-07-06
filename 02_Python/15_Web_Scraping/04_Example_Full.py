import requests
import bs4

base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
page_num = 1
base_url.format(page_num)

two_star_titles = []

for n in range(1,2):
    scrape_url = base_url.format(n)

    res = requests.get(scrape_url)
    soup = bs4.BeautifulSoup(res.text, 'lxml')

    all_book = soup.select(".product_pod")
    print(all_book)
    for book in all_book:
        if len(book.select(".star-rating.Two")) != 0: # or if "star-rating Two" in str(book)
            two_star_titles.append(book.select("a")[1]['title'])

for title in two_star_titles:
    print(title)