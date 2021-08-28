from PIL import Image

perc = 5

for i in range(1, 5):
    url = f"Images/Title Screen {i}.jpg"
    img = Image.open(url)
    w,h = img.width, img.height

    img = img.resize((int(w * perc / 100), int(h * perc / 100)))

    img.save(url.replace(".", " - Low Res."))