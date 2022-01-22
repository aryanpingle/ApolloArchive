from PIL import Image

file = "assets/images/Horizon - Zero Dawn.jpg"
img = Image.open(file)
img.resize((img.width // 2, img.height // 2)).save(file, "JPEG")