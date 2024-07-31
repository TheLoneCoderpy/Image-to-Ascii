from PIL import Image, ImageEnhance
from copy import deepcopy
import math
import os

ascii_brightness = " .:-=+*#%@"
ascii_num = len(ascii_brightness)

color = True
foreground = True
background = False

reset = {"fore": "\033[0m",  "back": "\033[0m"}
color_dict = {
    "black":            {"fore": "30", "back": "40",  "rgb": (0, 0, 0)},
    "red":              {"fore": "31", "back": "41",  "rgb": (127, 0, 0)},
    "green":            {"fore": "32", "back": "42",  "rgb": (0, 127, 0)},
    "yellow":           {"fore": "33", "back": "43",  "rgb": (127, 127, 0)},
    "blue":             {"fore": "34", "back": "44",  "rgb": (0, 0, 127)},
    "magenta":          {"fore": "35", "back": "45",  "rgb": (127, 0, 127)},
    "cyan":             {"fore": "36", "back": "46",  "rgb": (0, 127, 127)},
    "white":            {"fore": "37", "back": "47",  "rgb": (127, 127, 127)},
    "bright_black":     {"fore": "90", "back": "100", "rgb": (85, 85, 85)},
    "bright_red":       {"fore": "91", "back": "101", "rgb": (255, 85, 85)},
    "bright_green":     {"fore": "92", "back": "102", "rgb": (85, 255, 85)},
    "bright_yellow":    {"fore": "93", "back": "103", "rgb": (255, 255, 85)},
    "bright_blue":      {"fore": "94", "back": "104", "rgb": (85, 85, 255)},
    "bright_magenta":   {"fore": "95", "back": "105", "rgb": (255, 85, 255)},
    "bright_cyan":      {"fore": "96", "back": "106", "rgb": (85, 255, 255)},
    "bright_white":     {"fore": "97", "back": "107", "rgb": (255, 255, 255)},
    }

all_rgb = []
for k, v in color_dict.items():
    all_rgb.append(v["rgb"])

path = os.path.dirname(os.path.abspath(__file__))
img = Image.open(path + "/doom.jpg")
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.5)

dest_dim = (110, 40)
img = img.resize(dest_dim)
img_color = deepcopy(img)
img = img.convert("L")

ascii_string = ""
for y in range(img.size[1]):
    for x in range(img.size[0]):
        brightness = img.getpixel((x, y)) # 0 - 255
        color_pixel = img_color.getpixel((x, y))
        index = int((brightness / 255) * ascii_num - 1)
        start = ""
        if color:
            color_key = ""
            smallest_diff = 800
            for i, rgb in enumerate(all_rgb):
                diff = math.sqrt((color_pixel[0] - rgb[0])**2 + (color_pixel[1] - rgb[1])**2 + (color_pixel[2] - rgb[2])**2)
                if diff < smallest_diff:
                    smallest_diff = diff
                    color_key = list(color_dict.keys())[i]

        start = "\033["
        if foreground and not background:
            start += color_dict[color_key]["fore"]
        
        if background:
            if len(start) == 2:
                start += ";"
            start += color_dict[color_key]["back"]

        start += "m"

        if background:
            final_char = " "
        else:
            final_char = ascii_brightness[index]

        ascii_string += start + final_char + " " + "\033[0m"

    ascii_string += "\n"

print(ascii_string)