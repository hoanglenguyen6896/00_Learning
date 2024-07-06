import requests
import bs4

base_url = 'http://books.toscrape.com/catalogue/page-{}.html'
page_num = 1
base_url.format(page_num)

print(base_url)
print(base_url.format(page_num))

result = requests.get(base_url.format(1))
soup = bs4.BeautifulSoup(result.text, 'lxml')

product_pod = soup.select('.product_pod') # Return all classes = "product_pod"
print(product_pod)

three_star = 'star-rating Three' in example # This will return True/False

# Select class with title 'star-rating Three'
example.select(".star-rating.Three") # Need replace 'space' with 'dot'
# That will return a list, or empty list if no str match

# Find class="thing you want to find" > select(".thing.you.want.to.find")
# Find <a href="......"> </a> or <div ......       >>>>> select("a"), select("div")

# Grab title of book
res = example.select("a")[1]['title']
print(res)
res = example.select("a")[1].text
print(res)
