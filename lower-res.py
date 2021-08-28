from PIL import Image

url = "Images/Title Screen 4.jpg"
img = Image.open(url)
w,h = img.width, img.height

img = img.resize((w//4, h//4))

img.save(url.replace(".", " - Low Res."))