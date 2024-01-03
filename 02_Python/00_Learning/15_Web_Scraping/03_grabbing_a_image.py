import requests
import bs4

result = requests.get("https://en.wikipedia.org/wiki/Deep_Blue_(chess_computer)")
soup = bs4.BeautifulSoup(result.text, "lxml")

# Get title
res_title = soup.select('title')
print(res_title[0].getText())

# Get a img link
computer = soup.select('.thumbimage')[0]
img_from_soup = computer['src']

# Download/get img
img_to_get = 'https:' + img_from_soup
img_link = requests.get(img_link)

print(img_link.content)

# Save img: write bit
f = open('img_down_test.jpg', 'wb')
f.write(img_link.content)
f.close()