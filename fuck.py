from time import time
from PIL import Image
from random import randint, random

img = Image.open("Images/DatapointBackground.png").convert("RGBA")
data = img.getdata()

def process(rgba: list):
    greyscale = sum(rgba[:3]) // 3
    output = [0, 0, 0, 0] if rgba[-1] < 200 or greyscale >= 60 else [76, 69, 78, rgba[-1]]
    return tuple(map(lambda f: max(min(f, 255), 0), output))

stime = time()
newdata = list(map(process, data))
print(f"Completed in {time()-stime}s")

img.putdata(newdata)
img.save("Images/DatapointBackground-Transparent.png", "PNG")