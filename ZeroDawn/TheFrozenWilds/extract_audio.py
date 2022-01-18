from email.mime import audio
import requests
import re
import json
from time import time

template = """<div class="datapoint" description="{}" media-type="{}">
<div class="datapoint-title">
    <header>{}</header>
</div>
<div class="datapoint-content">
    <div class="datapoint-audio">
        <div class="play-button"></div>
        <div class="progress-bar"></div>
        <div class="ratio"></div>
    </div>
    <div class="datapoint-text">
        <text></text>
    </div>
</div>
</div>"""

stime = time()

def get_html(media_type, links):
    contents = []
    actual_contents = []
    for link in links:
        print(f"Starting {links.index(link)}")
        src = requests.get("https://horizon.fandom.com" + link).text
        # print("GOT SRC")
        title = re.search(r'(?<=data-source="title1">).*?(?=</h2>)', src).group()
        # print("GOT TITLE")
        content = re.findall(r'Contents?</span></h2>(.*?)\n*\s*(?=(?:<table class=)|(?:<h2><span class="mw-headline" id="Location">)|(?:<h2><span class="mw-headline" id="Trivia">))', src, flags=re.DOTALL)[0].strip()
        content = re.sub(r'<a.*?>(.*?)</a>', r'\1', content)
        content = re.sub(r'<p>(.*?)</p>', r'\1<br>', content, flags=re.DOTALL)
        content = re.sub(r'<dl>(.*?)</dl>', r'\1<br>', content, flags=re.DOTALL)
        content = re.sub(r"<dd>(.*?)</dd>", r"\1<br>", content, flags=re.DOTALL)
        # New
        content = content.replace("<br />", "<br>")
        content = content.replace("\n", "")

        # Description
        description = []
        index = src.find("Type</h3>")
        if src != -1:
            src = src[index:index+1200]
            type = re.search(r'<div class="pi-data-value pi-font">(.*?)</div>', src, re.DOTALL).group(1)
            type = re.sub(r'<a.*?>(.*?)</a>', r'\1', type)
            description.append(type)
            print(f"{type = }")
        index = src.find("Description</h3>")
        if index!=-1:
            desc = re.findall(r'<div class="pi-data-value pi-font">(.*?)</div>', src[index:], re.DOTALL)[0]
            desc = desc.replace("\"", "'")
            desc = re.sub(r'<a.*?>(.*?)</a>', r'\1', desc)
            desc = desc.replace("<br/>", "<br>")
            description.append(desc)
            print(f"{desc = }")
        index = src.find("Data Corruption</h3>")
        if index!=-1:
            corruption = "Data Corruption: " + re.findall(r'<div class="pi-data-value pi-font">(.*?)</div>', src[index:], re.DOTALL)[0]
            description.append(corruption)
            print(f"{corruption = }")
        contents.append(template.format("<br>".join(description), media_type, title))
        actual_contents.append(content)
    return (contents, actual_contents)

# Get Audio descriptions

audio_links = """<ol><li><a href="/wiki/Secret_Show" title="Secret Show">Secret Show</a></li>
<li><a href="/wiki/Dam_Family" title="Dam Family">Dam Family</a></li>
<li><a href="/wiki/Limited-Edition_Merch" title="Limited-Edition Merch">Limited-Edition Merch</a></li>
<li><a href="/wiki/Compensatory_Damages" title="Compensatory Damages">Compensatory Damages</a></li>
<li><a href="/wiki/Farewell_Tour" title="Farewell Tour">Farewell Tour</a></li>
<li><a href="/wiki/I_Understand,_Mr._Blevins" title="I Understand, Mr. Blevins">I Understand, Mr. Blevins</a></li>
<li><a href="/wiki/Final_Performance" title="Final Performance">Final Performance</a></li>
<li><a href="/wiki/Visitor_Center" title="Visitor Center">Visitor Center</a></li>
<li><a href="/wiki/Inspection_Failed" title="Inspection Failed">Inspection Failed</a></li>
<li><a href="/wiki/Return_to_Firebreak" title="Return to Firebreak">Return to Firebreak</a></li>
<li><a href="/wiki/Geothermal_Suspension" title="Geothermal Suspension">Geothermal Suspension</a></li>
<li><a href="/wiki/The_Conversation" title="The Conversation">The Conversation</a></li>
<li><a href="/wiki/Excessive_Secrecy" title="Excessive Secrecy">Excessive Secrecy</a></li>
<li><a href="/wiki/Firebreak_Upgrades" title="Firebreak Upgrades">Firebreak Upgrades</a></li>
<li><a href="/wiki/Supply_SNAFU" title="Supply SNAFU">Supply SNAFU</a></li>
<li><a href="/wiki/Menu_Prank" title="Menu Prank">Menu Prank</a></li>
<li><a href="/wiki/OMG_Blevins" title="OMG Blevins">OMG Blevins</a></li>
<li><a href="/wiki/Thanksgiving" title="Thanksgiving">Thanksgiving</a></li>
<li><a href="/wiki/Incommensurable" title="Incommensurable">Incommensurable</a></li>
<li><a href="/wiki/Holo-Lock_Reset" title="Holo-Lock Reset">Holo-Lock Reset</a></li>
<li><a href="/wiki/When_You_Wake" title="When You Wake">When You Wake</a></li>
<li><a href="/wiki/Last_Goodbye" title="Last Goodbye">Last Goodbye</a></li>
<li><a href="/wiki/Induced_Coma" title="Induced Coma">Induced Coma</a></li>
<li><a href="/wiki/The_Swarm" title="The Swarm">The Swarm</a></li>
<li><a href="/wiki/Oh-Point-Six" title="Oh-Point-Six">Oh-Point-Six</a></li></ol>"""

hologram_links = """<ol><li><a href="/wiki/The_Toast" title="The Toast">The Toast</a></li>
<li><a href="/wiki/HEPHAESTUS_Revealed" title="HEPHAESTUS Revealed">HEPHAESTUS Revealed</a></li>
<li><a href="/wiki/Instability" title="Instability">Instability</a></li></ol>"""

for [name, links] in [["AUDIO", audio_links], ["HOLOGRAM", hologram_links]]:
    links = re.findall(r'<a href="(.*?)"', links, flags=re.DOTALL)
    print(f"Starting {name}")
    with open('ZeroDawn/TheFrozenWilds/index.html', 'r', encoding="utf-8") as f:
        html = f.read()
    (datapoints_html, text_contents) = get_html(name[0], links)
    html = re.sub(rf"(?<=<!-- {name} DATAPOINTS -->).*?(?=<!-- END {name} DATAPOINTS -->)", "\n" + "".join(datapoints_html) + "\n", html, flags=re.DOTALL)
    with open("ZeroDawn/TheFrozenWilds/index.html", 'w', encoding="utf-8") as f:
        f.write(html)
    title = "-".join(list(map(str.capitalize, name.split())))
    with open(f"ZeroDawn/TheFrozenWilds/Texts/{title}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(text_contents, separators=(',', ';')))

    print(f"{time()-stime}s taken")