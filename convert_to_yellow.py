from time import time
from PIL import Image

# for name in ["audio", "hologram", "text", "scanned-glyphs"]:
#     img = Image.open(f"Images/datapoint-icon-{name}.png").convert("RGBA")
#     data = img.getdata()

#     def process(rgba: list):
#         alpha = rgba[-1]
#         g = sum(rgba[:3]) // 3
#         output = [255, 255, 160, alpha]
#         return tuple(map(lambda f: max(min(f, 255), 0), output))

#     stime = time()
#     newdata = list(map(process, data))
#     print(f"Completed in {time()-stime}s")

#     img.putdata(newdata)
#     img.save(f"Images/datapoint-icon-{name}-yellow.png", "PNG")

img = Image.open("Images/Background - Centered.png").convert("RGBA")
w,h = img.width,img.height
img = img.resize((w//2, h//2))
img.save("Images/Background-min.png", "PNG")