from time import time
from PIL import Image
from random import randint, random

img = Image.open("Images/Line.png").convert("RGBA")
data = img.getdata()

def process(rgba: list):
    grayscale = sum(rgba[:3]) // 3
    output = [255, 255, 150, grayscale - randint(0, 150)]
    return tuple(map(lambda f: max(min(f, 255), 0), output))

stime = time()
# newdata = [tuple(process(rgba)) for rgba in data]
newdata = list(map(process, data))
print(f"Completed in {time()-stime}s")

img.putdata(newdata)
img.save("Images/Line-Colored.png", "PNG")