import requests
import json
import re
from time import time
import pyperclip

template = """<div class="datapoint" description="{}">
<div class="datapoint-title">
    <header>{}</header>
</div>
<div class="datapoint-content">
    <div class="datapoint-text">
        <text></text>
    </div>
</div>
</div>"""

stime = time()

def get_html(links):
    contents = []
    actual_contents = []
    for link in links:
        print(f"Starting {links.index(link)}")
        src = requests.get("https://horizon.fandom.com" + link).text
        open("ZeroDawn/TheFrozenWilds/Buffer.txt", 'w', encoding='utf-8').write(src)
        title = re.search(r'(?<=data-source="title1">).*?(?=</h2>)', src).group()
        content = re.findall(r'Contents?</span></h2>(.*?)\n*\s*(?=(?:<table class=)|(?:<h2><span class="mw-headline" id="_?Location">)|(?:<h2><span class="mw-headline" id="Trivia">))', src, flags=re.DOTALL)[0].strip()
        content = re.sub(r'<a.*?>(.*?)</a>', r'\1', content)
        content = re.sub(r'<p>(.*?)</p>', r'\1<br><br>', content, flags=re.DOTALL)
        content = re.sub(r'<dl>(.*?)</dl>', r'\1<br>', content, flags=re.DOTALL)
        content = re.sub(r"<dd>(.*?)</dd>", r"\1<br>", content, flags=re.DOTALL)
        content = re.sub(r"<div class=\"poem\">(.*?)</div>", r"\1", content, flags=re.DOTALL) # Remove div class="poem"
        content = re.sub(r'(<br>)+$', '', content.strip()) # Remove ending break-lines
        content = re.sub(r'\\(.)', r'\\\\\1', content) # Not sure if needed but it doesn't break anything yet
        # New
        content = content.replace("<br />", "<br>")
        content = content.replace("\n", "")

        # Description
        description = []
        index = src.find("Type</h3>")
        if index != -1:
            src = src[index:index+1200]
            type = re.search(r'<div class="pi-data-value pi-font">(.*?)</div>', src, re.DOTALL).group(1)
            type = re.sub(r'<a.*?>(.*?)</a>', r'\1', type)
            description.append(type)
            print(f"{type = }")
        index = src.find("Description</h3>")
        if index!=-1:
            desc = re.findall(r'<div class="pi-data-value pi-font">(.*?)</div>', src[index:], re.DOTALL)[0]
            desc = desc.replace("\\", "\\\\")
            desc = desc.replace("\"", "'")
            desc = re.sub(r'<a.*?>(.*?)</a>', r'\1', desc)
            desc = desc.replace("<br/>", "<br>")
            print(f"{desc = }")
            description.append(desc)
        index = src.find("Data Corruption</h3>")
        if index!=-1:
            corruption = "Data Corruption: " + re.findall(r'<div class="pi-data-value pi-font">(.*?)</div>', src[index:], re.DOTALL)[0]
            print(f"{corruption = }")
            description.append(corruption)
        contents.append(template.format("<br>".join(description), title))
        actual_contents.append(content)
    return (contents, actual_contents)

text_quest_links = """<ol><li><a href="/wiki/Last_Girls_on_Earth" title="Last Girls on Earth">Last Girls on Earth</a></li>
<li><a href="/wiki/Ban_him!!!" title="Ban him!!!">Ban him!!!</a></li>
<li><a href="/wiki/Stage_2_Complete" title="Stage 2 Complete">Stage 2 Complete</a></li>
<li><a href="/wiki/CYAN_Access" title="CYAN Access">CYAN Access</a></li>
<li><a href="/wiki/Valves_101" title="Valves 101">Valves 101</a></li>
<li><a href="/wiki/The_Door,_Again" title="The Door, Again">The Door, Again</a></li>
<li><a href="/wiki/Security_Measures" title="Security Measures">Security Measures</a></li>
<li><a href="/wiki/That_Kiss" title="That Kiss">That Kiss</a></li>
<li><a href="/wiki/Kenny%27s_Homecoming" title="Kenny's Homecoming">Kenny's Homecoming</a></li>
<li><a href="/wiki/MIE_Assessment" title="MIE Assessment">MIE Assessment</a></li>
<li><a href="/wiki/Incident_Report_363-7" title="Incident Report 363-7">Incident Report 363-7</a></li>
<li><a href="/wiki/Creatures_of_Terror" title="Creatures of Terror">Creatures of Terror</a></li>
<li><a href="/wiki/Blast_from_the_Past" title="Blast from the Past">Blast from the Past</a></li>
<li><a href="/wiki/Holo_Redux" title="Holo Redux">Holo Redux</a></li></ol>"""

text_world_links = """<ol><li><a href="/wiki/OBSERVER_LOG_US-W-10" title="OBSERVER LOG US-W-10">OBSERVER LOG US-W-10</a></li>
<li><a href="/wiki/A_Summons_From_The_Claim" title="A Summons From The Claim">A Summons From The Claim</a></li>
<li><a href="/wiki/Our_Final_Two_Weeks" title="Our Final Two Weeks">Our Final Two Weeks</a></li>
<li><a href="/wiki/Goodbye_Grizzly" title="Goodbye Grizzly">Goodbye Grizzly</a></li>
<li><a href="/wiki/Emissions_Joyride" title="Emissions Joyride">Emissions Joyride</a></li>
<li><a href="/wiki/Yellowstone_Sux" title="Yellowstone Sux">Yellowstone Sux</a></li>
<li><a href="/wiki/Park_Status" title="Park Status">Park Status</a></li>
<li><a href="/wiki/Beverly_Hills_Terror_Attack" title="Beverly Hills Terror Attack">Beverly Hills Terror Attack</a></li>
<li><a href="/wiki/Return_to_Singapore" title="Return to Singapore">Return to Singapore</a></li>
<li><a href="/wiki/Proposal_Approved!" title="Proposal Approved!">Proposal Approved!</a></li>
<li><a href="/wiki/Will_tourists_return%3F" title="Will tourists return?">Will tourists return?</a></li>
<li><a href="/wiki/Lafayettes%27_Last_Supper" title="Lafayettes' Last Supper">Lafayettes' Last Supper</a></li>
<li><a href="/wiki/Last_Request" title="Last Request">Last Request</a></li></ol>"""

for [name, links] in [["TEXT WORLD", text_world_links], ["TEXT QUEST", text_quest_links]]:
    links = re.findall(r'<a href="(.*?)"', links, flags=re.DOTALL)
    print(f"Starting {name}")
    with open('ZeroDawn/TheFrozenWilds/index.html', 'r', encoding="utf-8") as f:
        html = f.read()
    (datapoints_html, text_contents) = get_html(links)
    html = re.sub(rf"(?<=<!-- {name} -->).*?(?=<!-- END {name} -->)", "".join(datapoints_html), html, flags=re.DOTALL)
    with open("ZeroDawn/TheFrozenWilds/index.html", 'w', encoding="utf-8") as f:
        f.write(html)
    title = "-".join(list(map(str.capitalize, name.split())))
    with open(f"ZeroDawn/TheFrozenWilds/Texts/{title}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(text_contents, separators=(',', ';')))

    print(f"{time()-stime}s taken")