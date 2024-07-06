from PIL import Image

mask_img = Image.open('mask.png')

# mask_img.show()

mask_crop = mask_img.crop((0,0,100,100))    # pos x (to right), pos y (to down), width, height

# mask_crop.show()

pencils = Image.open('pencils.jpg')

x = 0
y = 0
w = pencils.size[0] / 3
h = pencils.size[1]

pencils_crop = pencils.crop((x, y, w, h))
# pencils_crop.show()

pencils.paste(im = pencils_crop, box = (500, 500)) # Affect pencils
# pencils.show()

pencils_resize = pencils.resize((3000, 500))
# pencils_resize.show()

pencils_rotate = pencils.rotate(90)
pencils_rotate.show()