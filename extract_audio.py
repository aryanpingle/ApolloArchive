import requests
import re
from time import time
import pyperclip

template = """<div class="datapoint" description="{}">
<div class="datapoint-title">
    <header>{}</header>
</div>
<div class="datapoint-content">
    <div class="datapoint-audio">
        <div class="play-button"></div>
        <div class="progress-bar"></div>
    </div>
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
        content = re.findall(r'Content</span></h2>(.*?)\n*\s*(?=<table class=)', src, flags=re.DOTALL)[0].strip()
        content = re.sub(r'<a.*?>(.*?)</a>', r'\1', content)
        content = re.sub(r'<p>(.*?)</p>', r'\1<br>', content, flags=re.DOTALL)
        content = re.sub(r"<dd>(.*?)</dd>", r"\1<br>", content, flags=re.DOTALL)

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


links = ['/wiki/Log:_Connor_Chasson_(1)', '/wiki/Log:_Skylar_Rivera', '/wiki/Log:_Ella_Pontes', '/wiki/Log:_Jackson_Frye', '/wiki/Log:_Mia_Sayied', '/wiki/Log:_Connor_Chasson_(2)', '/wiki/Full_Stop', '/wiki/For_Director_Evans', '/wiki/R%26D/Lab_Retooling', '/wiki/Entangled_Waveforms', '/wiki/Regarding_The_Rumors', '/wiki/Comms_Log:_Lt._Murell', '/wiki/Comms_Log:_Sgt._Guliyev', '/wiki/Comms_Log:_Cpl._Mills', '/wiki/Comms_Log:_Sgt._Wandari', '/wiki/Reminder._Again.', '/wiki/Log:_Cpl._Acosta_(A)', '/wiki/Log:_Cpl._Acosta_(B)', '/wiki/Just_a_Little_Longer', '/wiki/So_Sorry!', '/wiki/Edited_And_Approved_1', '/wiki/Edited_And_Approved_2', '/wiki/I_Believe_In_You', '/wiki/Please_Reply!', '/wiki/Unit_Status_Report', '/wiki/Code_Nexus_Reminder', '/wiki/SecureCom_EVZD-XX1X011X', '/wiki/Wife', '/wiki/Meridian%27s_Fall', '/wiki/Prophecy', '/wiki/Itamen_Coddled', '/wiki/Without_Pity', '/wiki/Chosen_of_the_Sun', '/wiki/Interview:_Tom_Paech', '/wiki/Interview:_Travis_Tate', '/wiki/Interview:_Brad_Andac', '/wiki/Interview:_Susanne_Alpert', '/wiki/Interview:_Cpt._Okilo', '/wiki/Interview:_Ron_Felder', '/wiki/Interview:_Dr._Hsu-Vhey', '/wiki/Interview_2:_Brad_Andac', '/wiki/Interview_2:_Susanne_Alpert', '/wiki/Interview_2:_Ron_Felder', '/wiki/Log:_Tom_Paech', '/wiki/Log:_Christina_Hsu-Vhey', '/wiki/Log:_Travis_Tate_(1)', '/wiki/Herres_Testimonial', '/wiki/Code_Nexus_Problems', '/wiki/Lesson_57-6-A', '/wiki/GAIA_Prime_Arrival_Log', '/wiki/Log:_Charles_Ronson_(1)', '/wiki/Log:_Charles_Ronson_(2)', '/wiki/Log:_Margo_Sh%C4%95n', '/wiki/Rest_In_Peace', '/wiki/The_Future', '/wiki/The_Solution', '/wiki/Log:_Travis_Tate_(2)', '/wiki/Core_Control_Log', '/wiki/ELEUTHIA_Runtime_Check', '/wiki/First_Meeting', '/wiki/Buried_Shadow_(Datapoint)', '/wiki/Intercepted_Transmission', '/wiki/Recording_Device']

with open('Datapoints.html') as f:
    html = f.read()
html = re.sub(r"(?<=<!-- AUDIO DATAPOINTS -->).*?(?=<!-- END AUDIO DATAPOINTS -->)", "".join(get_html(links)), html, flags=re.DOTALL)
with open("Datapoints.html", 'w', encoding="utf-8") as f:
    f.write(html)

print(f"{time()-stime}s taken")

links = re.findall(r'<a href="(.*?)"', """<ol><li><a href="/wiki/Happy_Birthday_Isaac!" title="Happy Birthday Isaac!">Happy Birthday Isaac!</a></li>
<li><a href="/wiki/A_Message_for_Olin" title="A Message for Olin">A Message for Olin</a></li>
<li><a href="/wiki/Welcome_to_FAS" title="Welcome to FAS">Welcome to FAS</a></li>
<li><a href="/wiki/FAS-ACA3_Scarab_(Datapoint)" title="FAS-ACA3 Scarab (Datapoint)">FAS-ACA3 Scarab</a></li>
<li><a href="/wiki/FAS-FSP5_Khopesh_(Datapoint)" title="FAS-FSP5 Khopesh (Datapoint)">FAS-FSP5 Khopesh</a></li>
<li><a href="/wiki/FAS-BOR7_Horus_(Datapoint)" title="FAS-BOR7 Horus (Datapoint)">FAS-BOR7 Horus</a></li>
<li><a href="/wiki/Record:_31_Oct_2064" title="Record: 31 Oct 2064">Record: 31 Oct 2064</a></li>
<li><a href="/wiki/Record:_1_Nov_2064" title="Record: 1 Nov 2064">Record: 1 Nov 2064</a></li>
<li><a href="/wiki/Record:_3_Nov_2064" title="Record: 3 Nov 2064">Record: 3 Nov 2064</a></li>
<li><a href="/wiki/The_Bad_News" title="The Bad News">The Bad News</a></li>
<li><a href="/wiki/The_Good_News" title="The Good News">The Good News</a></li>
<li><a href="/wiki/Gaia_Log:_27_March_2065" title="Gaia Log: 27 March 2065">Gaia Log: 27 March 2065</a></li>
<li><a href="/wiki/Gaia_Log:_5_June_2065" title="Gaia Log: 5 June 2065">Gaia Log: 5 June 2065</a></li>
<li><a href="/wiki/Gaia_Log:_13_January_2066" title="Gaia Log: 13 January 2066">Gaia Log: 13 January 2066</a></li>
<li><a href="/wiki/E9B1_Incident_Log_A" title="E9B1 Incident Log A">E9B1 Incident Log A</a></li>
<li><a href="/wiki/E9B1_Incident_Log_B" title="E9B1 Incident Log B">E9B1 Incident Log B</a></li>
<li><a href="/wiki/E9B1_Incident_Log_C" title="E9B1 Incident Log C">E9B1 Incident Log C</a></li>
<li><a href="/wiki/E9B1_Incident_Log_D" title="E9B1 Incident Log D">E9B1 Incident Log D</a></li>
<li><a href="/wiki/Welcome_to_the_Lyceum" title="Welcome to the Lyceum">Welcome to the Lyceum</a></li>
<li><a href="/wiki/GAIA%27s_Dying_Plea" title="GAIA's Dying Plea">GAIA's Dying Plea</a></li>
<li><a href="/wiki/Elisabet_Sobeck_Memorial" title="Elisabet Sobeck Memorial">Elisabet Sobeck Memorial</a></li>
<li><a href="/wiki/Emergency_Recording" title="Emergency Recording">Emergency Recording</a></li></ol>""", re.DOTALL)

with open('Datapoints.html') as f:
    html = f.read()
html = re.sub(r"(?<=<!-- HOLOGRAM DATAPOINTS -->).*?(?=<!-- END HOLOGRAM DATAPOINTS -->)", "".join(get_html(links)), html, flags=re.DOTALL)
with open("Datapoints.html", 'w', encoding="utf-8") as f:
    f.write(html)

print(f"{time()-stime}s taken")