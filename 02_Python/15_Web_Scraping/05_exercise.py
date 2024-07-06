import bs4
import requests

base_url = 'http://quotes.toscrape.com/page/{}'

res = requests.get(base_url.format(1))
soup = bs4.BeautifulSoup(res.text, 'lxml')

# Print author
author_soup = soup.select(".author")

author_set = set()

for author_name in author_soup:
    author_set.add(author_name.text)

print(author_set)

# Print quote
quote_soup = soup.select('.text')

quote_list =[]

for quote in quote_soup:
    quote_list.append(quote.text)

print(quote_list)

# Print top ten tag
top_tag_soup = soup.select('.tag-item')
top_tag_list = []

for tag in top_tag_soup:
    top_tag_list.append(tag.text)

print(top_tag_)