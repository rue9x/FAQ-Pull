# javascript: make_printable(); on text faqs to get rid of the html
import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse

acceptable_consoles = dict()
acceptable_consoles = {
    "NES": "NES",
    "GB": "Gameboy",
    "GBC": "Gameboy Color",
    "GBA": "Game Boy Advance",
    "DS": "DS",
    "3DS": "3DS",
    "SNES": "SNES",
    "N64": "Nintendo 64",
    "GC":"Gamecube",
    "WII": "Wii",
    "SWITCH": "Nintendo Switch",
    "PSX": "PlayStation",
    "PSONE": "PlayStation",
    "PS": "PlayStaion",
    "PS2": "PlayStation 2",
    "PS3": "PlayStation 3",
    "PS4": "PlayStation 4",
    "PSP": "PSP",
    "VITA": "Vita",
    "PC": "PC",
    "XBOX": "Xbox",
    "XBOX360": "Xbox 360",
    "XBOXONE": "Xbox One"
}

def lookup_game(driver,chosen_console,game):
    console = chosen_console
    query=urllib.parse.quote_plus(game)
    driver.get("https://gamefaqs.gamespot.com/search?game="+query)
    driver.implicitly_wait(10)
    block_of_consoles = driver.find_elements_by_xpath("//div[@class='sr_product_name']/a[@class='log_search']")
    gamefound = False
    attempted_link = None

    for each_console in block_of_consoles:
        if console == each_console.text:
            chosen_block_of_consoles = each_console
            game_block = chosen_block_of_consoles.find_elements_by_xpath("../../../../div[@class='sr_header']/div[@class='sr_title']/div[@class='sr_name']/a[@class='log_search']")
            for each_game in game_block:
                # Standardize spaces and punctiation.
                site_game_standardize = each_game.text.upper()
                site_game_standardize = site_game_standardize.replace(" ","")
                site_game_standardize = site_game_standardize.replace(":","")
                site_game_standardize = site_game_standardize.replace("-","")
                site_game_standardize = site_game_standardize.replace("?","")
                site_game_standardize = site_game_standardize.replace("!","")
                site_game_standardize = site_game_standardize.replace("*","")
                site_game_standardize = site_game_standardize.replace("$","")
                site_game_standardize = site_game_standardize.replace("+","")
                
                search_game_standardize = game.upper()
                search_game_standardize = search_game_standardize.replace(" ","")
                search_game_standardize = search_game_standardize.replace(":","")
                search_game_standardize = search_game_standardize.replace("-","")
                search_game_standardize = search_game_standardize.replace("?","")
                search_game_standardize = search_game_standardize.replace("!","")
                search_game_standardize = search_game_standardize.replace("*","")
                search_game_standardize = search_game_standardize.replace("$","")
                search_game_standardize = search_game_standardize.replace("+","")
            
                if site_game_standardize == search_game_standardize:
                    attempted_link = chosen_block_of_consoles.get_attribute("href")
                    return attempted_link   

def display_help():
    global acceptable_consoles
    print ("Syntax: python3 "+__file__+"(console) (game)")
    print ("Where console can be any of the following: "+str(acceptable_consoles))

def setup_driver():
    options = Options()
    options.add_argument('--disable-javascript')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-extensions')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-logging")
    options.add_argument('--log-level=OFF')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    try:
        driver = webdriver.Chrome(options=options)
    except:
        driver = webdriver.Chrome(options=options, executable_path="c:\\chromedriver\\chromedriver.exe")
    return driver

def download_faq(driver, url, pid):
    try:
        driver.get(url)
        driver.implicitly_wait(30)
     
        textContent = driver.find_element_by_xpath("//div[@id='faqwrap']")
        fn = urllib.parse.quote_plus(sys.argv[2] + "_"+pid+".txt")
        with open (fn, 'w') as output:
            output.write(textContent.text)
        return fn
    except:
        return 0

def get_faq(driver,game_page, retval="list"):
    faq_page = game_page + "/faqs/"
    driver.get(faq_page)
    driver.implicitly_wait(10)
    contributor_tables = driver.find_elements_by_xpath("//div[@class='span8']//div[@class='body']//table[@class='contrib']")[0]

    guide_list = list()
    guide_dict = dict()
    highest_rated_objs = contributor_tables.find_elements_by_xpath("./tbody/tr/td[@class='ctitle']/i[@title='Highest Rated']")
    for each in highest_rated_objs:
        linkobj = each.find_element_by_xpath("../a")
        guide_url = linkobj.get_attribute("href")
        guide_name = linkobj.text
        guide_pid = guide_url.split("/")
        guide_pid = guide_pid[-1]
        guide_list.append(linkobj.get_attribute("href"))
        guide_dict[guide_pid] = dict()
        guide_dict[guide_pid]["guide_name"] = guide_name
        guide_dict[guide_pid]["guide_url"] = guide_url
        guide_dict[guide_pid]["rating"] = 5

    most_recommended_objs = contributor_tables.find_elements_by_xpath("./tbody/tr/td[@class='ctitle']/i[@title='Most Recommended']")
    for each in most_recommended_objs:
        linkobj = each.find_element_by_xpath("../a")
        linkobj = each.find_element_by_xpath("../a")
        guide_url = linkobj.get_attribute("href")
        guide_name = linkobj.text
        guide_pid = guide_url.split("/")
        guide_pid = guide_pid[-1]
        guide_list.append(linkobj.get_attribute("href"))
        guide_dict[guide_pid] = dict()
        guide_dict[guide_pid]["guide_name"] = guide_name
        guide_dict[guide_pid]["guide_url"] = guide_url
        guide_dict[guide_pid]["rating"] = 4
        
    alteast_complete_objs = contributor_tables.find_elements_by_xpath("./tbody/tr/td[@class='ctitle']/i[@title='Complete']")
    for each in   alteast_complete_objs:
        linkobj = each.find_element_by_xpath("../a")
        guide_url = linkobj.get_attribute("href")
        guide_name = linkobj.text
        guide_pid = guide_url.split("/")
        guide_pid = guide_pid[-1]
        guide_list.append(linkobj.get_attribute("href"))
        guide_dict[guide_pid] = dict()
        guide_dict[guide_pid]["guide_name"] = guide_name
        guide_dict[guide_pid]["guide_url"] = guide_url
        guide_dict[guide_pid]["rating"] = 3

    partial_objs = contributor_tables.find_elements_by_xpath("./tbody/tr/td[@class='ctitle']/i[@title='Partial']")
    for each in partial_objs:
        linkobj = each.find_element_by_xpath("../a")
        guide_url = linkobj.get_attribute("href")
        guide_name = linkobj.text
        guide_pid = guide_url.split("/")
        guide_pid = guide_pid[-1]
        guide_list.append(linkobj.get_attribute("href"))
        guide_dict[guide_pid] = dict()
        guide_dict[guide_pid]["guide_name"] = guide_name
        guide_dict[guide_pid]["guide_url"] = guide_url
        guide_dict[guide_pid]["rating"] = 2
    if retval == "list":
        return guide_list
    if retval == "dict":
        return guide_dict


def main():
    global acceptable_consoles
    try:

        the_console = (sys.argv[1])
        the_game (sys.argv[2])   
    except:
        display_help()
        sys.exit()
    # Evaluate all of the arguments
    if len(sys.argv) >= 1:
        if sys.argv[1].upper() in acceptable_consoles.keys():
            # Standardize the formatting.
            console = acceptable_consoles[sys.argv[1].upper()]
            pass # They picked a good console.
        else:
            # Also try letting them enter the full console name. Only fair.
            okay = False
            for each in acceptable_consoles.keys():
                if sys.argv[1].upper() == acceptable_consoles[each].upper():
                    okay = True
                    # Standardize the formatting.
                    console = acceptable_consoles[each]
            if okay == False:
                display_help()
                sys.exit()

    if len(sys.argv) >= 2:
        pass # They picked a game.
    else:
        display_help()
        sys.exit()

    driver = setup_driver()
    print ("Looking up "+sys.argv[2]+" on "+sys.argv[1]+"...")
    game_page = lookup_game(driver, console, sys.argv[2])

    if game_page == None:
        print ("No game page found.")
        quit()
    else:
        print ("Game found: "+each_console.text+" "+each_game.text+"!")
        print ("Looking for the best FAQ...")
        faq_dict = get_faq(driver,game_page,"dict")
        first_value = next(iter(faq_dict))
        print ("Downloading "+first_value)
        fn = download_faq(driver,faq_dict[first_value]["guide_url"],first_value)
        if fn != 0:
            print ("Downloaded to: "+fn)
        else:
            print ("Download failed!")
            driver.close()
            sys.exit()
    driver.close()
    print ("Done!")
    sys.exit()
main()
try:
    driver.close()
except:
    pass
sys.exit()
