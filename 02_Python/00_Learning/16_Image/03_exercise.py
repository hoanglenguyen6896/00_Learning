from PIL import Image

mask = Image.open('mask.png')
word_matrix = Image.open('word_matrix.png')

tup = word_matrix.size
mask = mask.resize(tup)

mask.putalpha(128)
word_matrix.paste(im = mask, box = (0,0), mask = mask)

word_matrix.show()