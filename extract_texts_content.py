# import re
# import json

# src = ""
# with open("Datapoints.html", encoding="utf-8") as f:
#     src = f.read()

# datatypes = ['AUDIO DATAPOINTS', 'HOLOGRAM DATAPOINTS', 'TEXT QUEST', 'TEXT WORLD', 'TEXT MACHINES', 'SCANNED GLYPHS']

# meme = []
# for dtype in datatypes:
#     section = re.search(fr'<!-- {dtype} -->(.*?)<!-- END {dtype} -->', src, flags=re.DOTALL).group()
#     contents = re.findall(r'<text>(.*?)</text>', section, flags=re.DOTALL)
#     contents = list(map(lambda x: re.sub(r'\s+', ' ', x.strip()), contents))
#     meme.append(contents)

# with open("meme.js", 'w', encoding='utf-8') as f:
#     f.write("let cumlord = " + json.dumps(meme))

import re

with open('Datapoints.html', encoding='utf-8') as f:
    data = f.read()

data = re.sub(r'<text>.*?</text>', '<text></text>', data, flags=re.DOTALL)

with open('Datapoints2.html', 'w', encoding='utf-8') as f:
    f.write(data)