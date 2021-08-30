from PIL import Image

img = Image.open("Images/favicon.png")

img = img.resize((64, 64))

img.save("Images/favicon.ico", "ICO")