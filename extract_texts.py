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
        title = re.search(r'(?<=data-source="title1">).*?(?=</h2>)', src).group()
        content = re.findall(r'Content</span></h2>(.*?)\n*\s*(?=(?:<table class=)|(?:<h2><span class="mw-headline" id="_?Location">)|(?:<h2><span class="mw-headline" id="Trivia">))', src, flags=re.DOTALL)[0].strip()
        content = re.sub(r'<a.*?>(.*?)</a>', r'\1', content)
        content = re.sub(r'<p>(.*?)</p>', r'\1<br><br>', content, flags=re.DOTALL)
        content = re.sub(r'<dl>(.*?)</dl>', r'\1<br>', content, flags=re.DOTALL)
        content = re.sub(r"<dd>(.*?)</dd>", r"\1<br>", content, flags=re.DOTALL)
        content = re.sub(r"<div class=\"poem\">(.*?)</div>", r"\1", content, flags=re.DOTALL) # Remove div class="poem"
        content = re.sub(r'(<br>)+$', '', content.strip()) # Remove ending break-lines
        content = re.sub(r'\\(.)', r'\\\\\1', content) # Not sure if needed but it doesn't break anything yet

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

text_quest_links = """<ol><li><a href="/wiki/All_Good_Things..." title="All Good Things...">All Good Things...</a></li>
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
<li><a href="/wiki/Gaia_Log:_3_Feb_2065_R" title="Gaia Log: 3 Feb 2065 R">Gaia Log: 3 Feb 2065 R</a></li></ol>"""

text_world_links = """<ol><li><a href="/wiki/Refugee_museum_opens" title="Refugee museum opens">Refugee museum opens</a></li>
<li><a href="/wiki/%22Haere_Mai%22" title="&quot;Haere Mai&quot;">"Haere Mai"</a></li>
<li><a href="/wiki/Schott_v._Frost" title="Schott v. Frost">Schott v. Frost</a></li>
<li><a href="/wiki/Jeff_Andreatis_Show" title="Jeff Andreatis Show">Jeff Andreatis Show</a></li>
<li><a href="/wiki/UK_vets_struggle" title="UK vets struggle">UK vets struggle</a></li>
<li><a href="/wiki/Leaks_sparks_fears" title="Leaks sparks fears">Leaks sparks fears</a></li>
<li><a href="/wiki/Hartz_wins_Bahamas" title="Hartz wins Bahamas">Hartz wins Bahamas</a></li>
<li><a href="/wiki/1st_Amendment_Virtual%3F" title="1st Amendment Virtual?">1st Amendment Virtual?</a></li>
<li><a href="/wiki/Harriet_Choi_Dies" title="Harriet Choi Dies">Harriet Choi Dies</a></li>
<li><a href="/wiki/Mourn_mosquitoes%3F" title="Mourn mosquitoes?">Mourn mosquitoes?</a></li>
<li><a href="/wiki/Turing_Act_criticized" title="Turing Act criticized">Turing Act criticized</a></li>
<li><a href="/wiki/Who_Did_This%3F_86" title="Who Did This? 86">Who Did This? #86</a></li>
<li><a href="/wiki/Lure_of_the_Real" title="Lure of the Real">Lure of the Real</a></li>
<li><a href="/wiki/Destin_folds" title="Destin folds">Destin folds</a></li>
<li><a href="/wiki/Reiker_Building%3F" title="Reiker Building?">Reiker Building?</a></li>
<li><a href="/wiki/Get_Ti-D-O_Started!" title="Get Ti-D-O Started!">Get Ti-D-O Started!</a></li>
<li><a href="/wiki/Robar_is_coming!" title="Robar is coming!">Robar is coming!</a></li>
<li><a href="/wiki/EZVenue_Staffing" title="EZVenue Staffing">EZVenue Staffing</a></li>
<li><a href="/wiki/Inebri8_available!" title="Inebri8 available!">Inebri8 available!</a></li>
<li><a href="/wiki/RPGreet!" title="RPGreet!">RPGreet!</a></li>
<li><a href="/wiki/Get_Tactile!" title="Get Tactile!">Get Tactile!</a></li>
<li><a href="/wiki/Summer_Sale!_YumNow!" title="Summer Sale! YumNow!">Summer Sale! YumNow!</a></li>
<li><a href="/wiki/It%27s_PizzaVeet!" title="It's PizzaVeet!">It's PizzaVeet!</a></li>
<li><a href="/wiki/DO_NOT_IGNORE!" title="DO NOT IGNORE!">DO NOT IGNORE!</a></li>
<li><a href="/wiki/VeetEats!" title="VeetEats!">VeetEats!</a></li>
<li><a href="/wiki/VertiVIP_Program" title="VertiVIP Program">VertiVIP Program</a></li>
<li><a href="/wiki/Hey_Subscriber!" title="Hey Subscriber!">Hey Subscriber!</a></li>
<li><a href="/wiki/Greece_is_Calling" title="Greece is Calling">Greece is Calling</a></li>
<li><a href="/wiki/AVOID_THE_TOUR!" title="AVOID THE TOUR!">AVOID THE TOUR!</a></li>
<li><a href="/wiki/We_Were_Indonesia" title="We Were Indonesia">We Were Indonesia</a></li>
<li><a href="/wiki/Grey_Swarms_Diary" title="Grey Swarms Diary">Grey Swarms Diary</a></li>
<li><a href="/wiki/Metal_vs_Meat!" title="Metal vs Meat!">Metal vs Meat!</a></li>
<li><a href="/wiki/Vani_In_Concert" title="Vani In Concert">Vani In Concert</a></li>
<li><a href="/wiki/Holo_Listings" title="Holo Listings">Holo Listings</a></li>
<li><a href="/wiki/Tormented_Giveaway!" title="Tormented Giveaway!">Tormented Giveaway!</a></li>
<li><a href="/wiki/Naysay_Doom_(Datapoint)" title="Naysay Doom (Datapoint)">Naysay Doom</a></li>
<li><a href="/wiki/Course_Listing,_2063" title="Course Listing, 2063">Course Listing, 2063</a></li>
<li><a href="/wiki/$$$_With_MechBooker!" title="$$$ With MechBooker!">$$$ With MechBooker!</a></li>
<li><a href="/wiki/Holoskins_Daily_6/6/61" title="Holoskins Daily 6/6/61">Holoskins Daily 6/6/61</a></li>
<li><a href="/wiki/All_The_Same" title="All The Same">All The Same</a></li>
<li><a href="/wiki/China-Sick" title="China-Sick">China-Sick</a></li>
<li><a href="/wiki/She%27s_The_One" title="She's The One">She's The One</a></li>
<li><a href="/wiki/Mexico" title="Mexico">Mexico</a></li>
<li><a href="/wiki/Cram" title="Cram">Cram</a></li>
<li><a href="/wiki/Supplier" title="Supplier">Supplier</a></li>
<li><a href="/wiki/Sleeper" title="Sleeper">Sleeper</a></li>
<li><a href="/wiki/Idiot_Army_(Datapoint)" title="Idiot Army (Datapoint)">Idiot Army</a></li>
<li><a href="/wiki/Holo-Haunting" title="Holo-Haunting">Holo-Haunting</a></li>
<li><a href="/wiki/Luna_Here_I_Come" title="Luna Here I Come">Luna Here I Come</a></li>
<li><a href="/wiki/Log:_3/3/64" title="Log: 3/3/64">Log: 3/3/64</a></li>
<li><a href="/wiki/I_Must_Thank_You" title="I Must Thank You">I Must Thank You</a></li>
<li><a href="/wiki/To_All_Jessifans" title="To All Jessifans">To All Jessifans</a></li>
<li><a href="/wiki/Chocolate_Box_Log" title="Chocolate Box Log">Chocolate Box Log</a></li>
<li><a href="/wiki/Log:_5/18/63" title="Log: 5/18/63">Log: 5/18/63</a></li>
<li><a href="/wiki/SPECIAL_ORDERS" title="SPECIAL ORDERS">SPECIAL ORDERS</a></li>
<li><a href="/wiki/What_scares_me..." title="What scares me...">What scares me...</a></li>
<li><a href="/wiki/Do_Your_Part" title="Do Your Part">Do Your Part</a></li>
<li><a href="/wiki/Your_%22Gift%22" title="Your &quot;Gift&quot;">Your "Gift"</a></li>
<li><a href="/wiki/No_subject" title="No subject"> [No subject]</a></li>
<li><a href="/wiki/This_Sucks" title="This Sucks">This Sucks</a></li>
<li><a href="/wiki/Phantom_Limbs" title="Phantom Limbs">Phantom Limbs</a></li>
<li><a href="/wiki/Just_Got_Back" title="Just Got Back">Just Got Back</a></li>
<li><a href="/wiki/Odyssey_Injustice%3F" title="Odyssey Injustice?">Odyssey Injustice?</a></li>
<li><a href="/wiki/Odyssey_Drives_Ready" title="Odyssey Drives Ready">Odyssey Drives Ready</a></li>
<li><a href="/wiki/Odyssey_to_Nowhere" title="Odyssey to Nowhere">Odyssey to Nowhere</a></li>
<li><a href="/wiki/Dalgaard_on_FZ" title="Dalgaard on FZ">Dalgaard on FZ</a></li>
<li><a href="/wiki/Odyssey_ready%3F" title="Odyssey ready?">Odyssey ready?</a></li></ol>"""

text_machines_links = """<ol><li><a href="/wiki/OBSERVER_LOG_US-W-17" title="OBSERVER LOG US-W-17">OBSERVER LOG US-W-17</a></li>
<li><a href="/wiki/OBSERVER_LOG_US-W-18" title="OBSERVER LOG US-W-18">OBSERVER LOG US-W-18</a></li>
<li><a href="/wiki/OBSERVER_LOG_US-W-19" title="OBSERVER LOG US-W-19">OBSERVER LOG US-W-19</a></li>
<li><a href="/wiki/OBSERVER_LOG_US-W-20" title="OBSERVER LOG US-W-20">OBSERVER LOG US-W-20</a></li>
<li><a href="/wiki/OBSERVER_LOG_US-W-21" title="OBSERVER LOG US-W-21">OBSERVER LOG US-W-21</a></li>
<li><a href="/wiki/M/SIGMA_CORE_LOG_763E" title="M/SIGMA CORE LOG 763E">M/SIGMA CORE LOG 763E</a></li>
<li><a href="/wiki/M/RHO_CORE_LOG_653Z" title="M/RHO CORE LOG 653Z">M/RHO CORE LOG 653Z</a></li>
<li><a href="/wiki/M/THETA_CORE_LOG_893V" title="M/THETA CORE LOG 893V">M/THETA CORE LOG 893V</a></li>
<li><a href="/wiki/M/XI_CORE_LOG_231L" title="M/XI CORE LOG 231L">M/XI CORE LOG 231L</a></li>
<li><a href="/wiki/M/ALL-US-W_CM_LOG_329G" title="M/ALL-US-W CM LOG 329G">M/ALL-US-W CM LOG 329G</a></li></ol>"""

text_scanned_glyphs_links = """<ol><li><a href="/wiki/The_Sun-Kings" title="The Sun-Kings">The Sun-Kings</a></li>
<li><a href="/wiki/Record_of_Redmaw_2" title="Record of Redmaw 2">Record of Redmaw 2</a></li>
<li><a href="/wiki/History_of_Sunfall" title="History of Sunfall">History of Sunfall</a></li>
<li><a href="/wiki/Bylaws_of_the_Lodge" title="Bylaws of the Lodge">Bylaws of the Lodge</a></li>
<li><a href="/wiki/The_Claim_(Datapoint)" title="The Claim (Datapoint)">The Claim</a></li>
<li><a href="/wiki/Founding_Of_Meridian" title="Founding Of Meridian">Founding Of Meridian</a></li>
<li><a href="/wiki/The_Liberation" title="The Liberation">The Liberation</a></li>
<li><a href="/wiki/The_Mad_Sun-King" title="The Mad Sun-King">The Mad Sun-King</a></li>
<li><a href="/wiki/The_Sun_Faith" title="The Sun Faith">The Sun Faith</a></li>
<li><a href="/wiki/Legendary_Hunts" title="Legendary Hunts">Legendary Hunts</a></li>
<li><a href="/wiki/Record_of_Redmaw_1" title="Record of Redmaw 1">Record of Redmaw 1</a></li>
<li><a href="/wiki/Olin%27s_Journal" title="Olin's Journal">Olin's Journal</a></li>
<li><a href="/wiki/The_Banuk" title="The Banuk">The Banuk</a></li>
<li><a href="/wiki/The_Nora" title="The Nora">The Nora</a></li>
<li><a href="/wiki/The_Derangement_(Datapoint)" title="The Derangement (Datapoint)">The Derangement</a></li>
<li><a href="/wiki/The_Old_Ones_(Datapoint)" title="The Old Ones (Datapoint)">The Old Ones</a></li>
<li><a href="/wiki/Captains_and_Capers" title="Captains and Capers">Captains and Capers</a></li>
<li><a href="/wiki/The_Forbidden_West" title="The Forbidden West">The Forbidden West</a></li></ol>"""

for [name, links] in [["SCANNED GLYPHS", text_scanned_glyphs_links]]:
    links = re.findall(r'<a href="(.*?)"', links, flags=re.DOTALL)
    print(f"Starting {name}")
    with open('Datapoints.html', 'r', encoding="utf-8") as f:
        html = f.read()
    html = re.sub(rf"(?<=<!-- {name} -->).*?(?=<!-- END {name} -->)", "".join(get_html(links)), html, flags=re.DOTALL)
    with open("Datapoints.html", 'w', encoding="utf-8") as f:
        f.write(html)

    print(f"{time()-stime}s taken")