from PIL import Image
import statistics
import pyautogui as gui

img = gui.screenshot(region = (10, 70+10, 1000, 1000 * 9 // 16))

data = img.getdata()
def lerp(val, lb, ub, lv, uv):
    return lv + (val-lb)*(uv-lv)/(ub-lb)
def process(rgba):
    rgba = list(rgba)
    rgba = [255, 255, 255, rgba[-1]]
    # rgba = [255, 255, 255, rgba[-1]]
    return tuple(rgba)
newdata = list(map(process, data))
img.putdata(newdata)
img.show()
# img.save("Assets/Images/Horizon ZD.png", "PNG")