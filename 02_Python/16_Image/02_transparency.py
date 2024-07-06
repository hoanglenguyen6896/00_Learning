from PIL import Image

red = Image.open('red_color.jpg')
purple = Image.open('purple.png')

print(red.mode)
print(purple.mode)

# red.putalpha(128)
# red.show()
# red.putalpha(0)
# red.show()
red.putalpha(128)
purple.putalpha(128)
purple.paste(im = red, box = (0,0), mask = red)

purple.show()

purple.save('purple_new.png')