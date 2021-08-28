from PIL import Image

for i in range(1, 5):
    url = f"Images/Title Screen {i}.jpg"
    img = Image.open(url)
    w,h = img.width, img.height

    img = img.resize((w//5, h//5))

    img.save(url.replace(".", " - Low Res."))