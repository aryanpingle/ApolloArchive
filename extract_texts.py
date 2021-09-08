import requests
import re
from time import time
import pyperclip

template = """<div class="datapoint" description="{}">
<div class="datapoint-title">
    <header>{}</header>
</div>
<div class="datapoint-content">
    <div class="datapoint-text">
        <text>
        {}
        </text>
    </div>
</div>
</div>"""

stime = time()

def get_html(links):
    contents = []
    for link in links:
        print(f"Starting {links.index(link)}")
        src = requests.get("https://horizon.fandom.com" + link).text
        # print("GOT SRC")
        title = re.search(r'(?<=data-source="title1">).*?(?=</h2>)', src).group()
        # print("GOT TITLE")
        content = re.findall(r'Content</span></h2>(.*?)\n*\s*(?=(?:<table class=)|(?:<h2><span class="mw-headline" id="Location">)|(?:<h2><span class="mw-headline" id="Trivia">))', src, flags=re.DOTALL)[0].strip()
        content = re.sub(r'<a.*?>(.*?)</a>', r'\1', content)
        content = re.sub(r'<p>(.*?)</p>', r'\1<br><br>', content, flags=re.DOTALL)
        content = re.sub(r'<dl>(.*?)</dl>', r'\1<br>', content, flags=re.DOTALL)
        content = re.sub(r"<dd>(.*?)</dd>", r"\1<br>", content, flags=re.DOTALL)
        content = re.sub(r'\\(.)', r'\\\\\1', content)
        # print(content)

        # Description
        description = []
        index = src.index("Type</h3>")
        src = src[index:index+1200]
        type = re.search(r'<div class="pi-data-value pi-font">(.*?)</div>', src, re.DOTALL).group(1)
        type = re.sub(r'<a.*?>(.*?)</a>', r'\1', type)
        description.append(type)
        print(type)
        index = src.find("Description</h3>")
        if index!=-1:
            desc = re.findall(r'<div class="pi-data-value pi-font">(.*?)</div>', src[index:], re.DOTALL)[0]
            desc = desc.replace("\\", "\\\\")
            desc = desc.replace("\"", "'")
            desc = re.sub(r'<a.*?>(.*?)</a>', r'\1', desc)
            desc = desc.replace("<br/>", "<br>")
            print(desc)
            description.append(desc)
        index = src.find("Data Corruption</h3>")
        if index!=-1:
            corruption = "Data Corruption: " + re.findall(r'<div class="pi-data-value pi-font">(.*?)</div>', src[index:], re.DOTALL)[0]
            print(corruption)
            description.append(corruption)
        contents.append(template.format("<br>".join(description), title, content))
    return contents

links = re.findall(r'<a href="(.*?)"', """<ol><li><a href="/wiki/All_Good_Things..." title="All Good Things...">All Good Things...</a></li>
<li><a href="/wiki/Bio:_Elisabet_Sobeck" title="Bio: Elisabet Sobeck">Bio: Elisabet Sobeck</a></li>
<li><a href="/wiki/Bio:_Ted_Faro" title="Bio: Ted Faro">Bio: Ted Faro</a></li>
<li><a href="/wiki/History:_FAS" title="History: FAS">History: FAS</a></li>
<li><a href="/wiki/Definition:_Corporation" title="Definition: Corporation">Definition: Corporation</a></li>
<li><a href="/wiki/Reception_Log" title="Reception Log">Reception Log</a></li>
<li><a href="/wiki/Re:_Complaint" title="Re: Complaint">Re: Complaint</a></li>
<li><a href="/wiki/Banda_Sea_Incident" title="Banda Sea Incident">Banda Sea Incident</a></li>
<li><a href="/wiki/All_Hands_on_Deck" title="All Hands on Deck">All Hands on Deck</a></li>
<li><a href="/wiki/Spiritual_Summit" title="Spiritual Summit">Spiritual Summit</a></li>
<li><a href="/wiki/FAS_Campus_Log" title="FAS Campus Log">FAS Campus Log</a></li>
<li><a href="/wiki/Log:_Cpl._Sarai_(A)" title="Log: Cpl. Sarai (A)">Log: Cpl. Sarai (A)</a></li>
<li><a href="/wiki/Log:_Cpl._Sarai_(B)" title="Log: Cpl. Sarai (B)">Log: Cpl. Sarai (B)</a></li>
<li><a href="/wiki/USRC_Deployment_Records" title="USRC Deployment Records">USRC Deployment Records</a></li>
<li><a href="/wiki/Biosphere_Degradation" title="Biosphere Degradation">Biosphere Degradation</a></li>
<li><a href="/wiki/We_Need_Support_Too!" title="We Need Support Too!">We Need Support Too!</a></li>
<li><a href="/wiki/Another_Incident" title="Another Incident">Another Incident</a></li>
<li><a href="/wiki/Sound_Proofing%3F" title="Sound Proofing?">Sound Proofing?</a></li>
<li><a href="/wiki/Restock_Or_Else..." title="Restock Or Else...">Restock Or Else...</a></li>
<li><a href="/wiki/Counselor_Guidelines_(1)" title="Counselor Guidelines (1)">Counselor Guidelines (1)</a></li>
<li><a href="/wiki/Counselor_Guidelines_(2)" title="Counselor Guidelines (2)">Counselor Guidelines (2)</a></li>
<li><a href="/wiki/Make_Your_Selection" title="Make Your Selection">Make Your Selection</a></li>
<li><a href="/wiki/Encapsulated_DNA" title="Encapsulated DNA">Encapsulated DNA</a></li>
<li><a href="/wiki/APOLLO_Update" title="APOLLO Update">APOLLO Update</a></li>
<li><a href="/wiki/Simulation_Results" title="Simulation Results">Simulation Results</a></li>
<li><a href="/wiki/Full_Steam_Ahead" title="Full Steam Ahead">Full Steam Ahead</a></li>
<li><a href="/wiki/%22Noise_Complaints%22" title="&quot;Noise Complaints&quot;">"Noise Complaints"</a></li>
<li><a href="/wiki/HADES_Protocol" title="HADES Protocol">HADES Protocol</a></li>
<li><a href="/wiki/Archive_Abuse" title="Archive Abuse">Archive Abuse</a></li>
<li><a href="/wiki/Cradle_Sealed" title="Cradle Sealed">Cradle Sealed</a></li>
<li><a href="/wiki/Cradle_Servitor_Personae" title="Cradle Servitor Personae">Cradle Servitor Personae</a></li>
<li><a href="/wiki/FZ_Chambers" title="FZ Chambers">FZ Chambers</a></li>
<li><a href="/wiki/Odyssey_Has_Failed" title="Odyssey Has Failed">Odyssey Has Failed</a></li>
<li><a href="/wiki/ARTEMIS_Status" title="ARTEMIS Status">ARTEMIS Status</a></li>
<li><a href="/wiki/Chamber_B1-001" title="Chamber B1-001">Chamber B1-001</a></li>
<li><a href="/wiki/GESTATION-E9B1" title="GESTATION-E9B1">[GESTATION-E9B1]</a></li>
<li><a href="/wiki/Operations_Log" title="Operations Log">Operations Log</a></li>
<li><a href="/wiki/NURSERY-E9B1" title="NURSERY-E9B1">[NURSERY-E9B1]</a></li>
<li><a href="/wiki/KINDERGARTEN-E9B1" title="KINDERGARTEN-E9B1">[KINDERGARTEN-E9B1]</a></li>
<li><a href="/wiki/Sobeck_Journal,_11-19-64" title="Sobeck Journal, 11-19-64">Sobeck Journal, 11-19-64</a></li>
<li><a href="/wiki/Sobeck_Journal,_7-16-65" title="Sobeck Journal, 7-16-65">Sobeck Journal, 7-16-65</a></li>
<li><a href="/wiki/Sobeck_Journal,_10-31-65" title="Sobeck Journal, 10-31-65">Sobeck Journal, 10-31-65</a></li>
<li><a href="/wiki/Sobeck_Journal,_1-15-66" title="Sobeck Journal, 1-15-66">Sobeck Journal, 1-15-66</a></li>
<li><a href="/wiki/Gaia_Log:_3_Feb_2065" title="Gaia Log: 3 Feb 2065">Gaia Log: 3 Feb 2065</a></li>
<li><a href="/wiki/Sobeck_Journal,_11-19-64_R" title="Sobeck Journal, 11-19-64 R">Sobeck Journal, 11-19-64 R</a></li>
<li><a href="/wiki/Sobeck_Journal,_7-16-65_R" title="Sobeck Journal, 7-16-65 R">Sobeck Journal, 7-16-65 R</a></li>
<li><a href="/wiki/Sobeck_Journal,_10-31-65_R" title="Sobeck Journal, 10-31-65 R">Sobeck Journal, 10-31-65 R</a></li>
<li><a href="/wiki/Sobeck_Journal,_1-15-66_R" title="Sobeck Journal, 1-15-66 R">Sobeck Journal, 1-15-66 R</a></li>
<li><a href="/wiki/Dervahl%27s_Journal" title="Dervahl's Journal">Dervahl's Journal</a></li>
<li><a href="/wiki/Tattered_Letter" title="Tattered Letter">Tattered Letter</a></li>
<li><a href="/wiki/Ultraweave_Progress" title="Ultraweave Progress">Ultraweave Progress</a></li>
<li><a href="/wiki/Ultraweave_Trials" title="Ultraweave Trials">Ultraweave Trials</a></li>
<li><a href="/wiki/Gaia_Log:_3_Feb_2065_R" title="Gaia Log: 3 Feb 2065 R">Gaia Log: 3 Feb 2065 R</a></li></ol>""", re.DOTALL)

with open('Datapoints.html', 'r', encoding="utf-8") as f:
    html = f.read()
html = re.sub(r"(?<=<!-- TEXT QUEST -->).*?(?=<!-- END TEXT QUEST -->)", "".join(get_html(links)), html, flags=re.DOTALL)
with open("Datapoints.html", 'w', encoding="utf-8") as f:
    f.write(html)

print(f"{time()-stime}s taken")