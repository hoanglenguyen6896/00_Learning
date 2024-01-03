import requests
import bs4

result = requests.get("https://en.wikipedia.org/wiki/Grace_Hopper")
soup = bs4.BeautifulSoup(result.text, "lxml")

# print(soup)

# Get title
res_title = soup.select('title')
print(res_title)
print(res_title[0])
print(res_title[0].getText())

class_result = soup.select('.toctext')
# print(soup.select('.toctext'))
for item in class_result:
    print(item.text)
