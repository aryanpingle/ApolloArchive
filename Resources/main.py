import json
import re

src = open("Datapoints.html", encoding='utf-8').read()

sections = re.findall(r'(<!-- (.*?) -->.*?<!-- END \2 -->)', src, flags=re.DOTALL)
section_titles = [i[1].replace(" DATAPOINTS", "").capitalize().split(" ") for i in sections]
section_titles = [list(map(str.capitalize, i)) for i in section_titles]
section_titles = ["-".join(i) for i in section_titles]
texts = [re.findall(r'(?<=<text>).*?(?=</text>)', section[0], flags=re.DOTALL) for section in sections]
texts = [list(map(lambda x: x.strip("\n "), i)) for i in texts]

for index, title in enumerate(section_titles):
    json.dump(texts[index], open(f"Texts/{title}.json", 'w', encoding='utf-8'))

src = re.sub(r'(?<=<text>).*?(?=</text>)', '', src, flags=re.DOTALL)
open("Datapoints (COPY).html", 'w', encoding='utf-8').write(src)