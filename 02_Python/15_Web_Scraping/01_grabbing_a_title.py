import requests
import bs4

result = requests.get("https://example.com")
print(type(result))

soup = bs4.BeautifulSoup(result.text, "lxml")

# print(soup)

# Get title
res_title = soup.select('title')
print(res_title)
print(res_title[0])
print(res_title[0].getText())

# Get paragraph
res_para = soup.select('p')
print(res_para)
print(res_para[0].getText())
