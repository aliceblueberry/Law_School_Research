#python3 grab.py
#Part 1
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#Waits Package
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#ActionChains
from selenium.webdriver import ActionChains

import sys
import time
#Part 2
import csv
#Part 3
import os
import subprocess
#Getting fancy
from progress.bar import Bar

bar = Bar('Importing', max =10)

bar.next()
print("  Check Download Path")
if os.path.exists("LawProjectDownloadFolder") is False:
    os.mkdir("LawProjectDownloadFolder")
currentPath = os.getcwd();
downloadpath = os.path.join(currentPath, "LawProjectDownloadFolder")
bar.next()
print("  File will store in " + downloadpath)
options = webdriver.ChromeOptions()
#This options can run chrome driver headless
#options.add_argument("--headless")
prefs = {
    "download.default_directory":downloadpath,
        "directory_upgrade": True
    }
options.add_experimental_option("prefs", prefs)
bar.next()
print("  Setting up Chrome Driver")
browser = webdriver.Chrome(executable_path = './chromedriver', chrome_options=options);
# The website we wish to retrieve information from.
bar.next()
print("  Go to URL")
browser.get("https://www.dcbar.org/attorney-discipline/disciplinary-decisions.cfm");
try:
    bar.next()
    print("  Waiting the Page to load");
    element = WebDriverWait(browser, 10).until(
                                               EC.presence_of_element_located((By.ID, "startDate"))
                                               )
finally:
    bar.next()
    print("  Page loaded");
    date_from = browser.find_element(By.ID, "startDate");
    #Wait for the thing to load fully. You can tweak it if you like.
    #First Step: Extract everything, and throw them in a CSV file.
    time.sleep(3);
    date_from.click();
    date_from.clear();
    #NOTICE: PLEASE CHANGE THIS ENTRY.
    date_from.send_keys("1900/01/01");
    date_from.send_keys(Keys.ENTER);
    time.sleep(2);
    elems = browser.find_elements(By.XPATH, '//form')
    print(len(elems))
    #Now put everything here into CSV. But now, try to store them.
    array_for_everything_container = []
    all_the_links = []
    #in-var
    counter = 0
    #click through all hrefs
for elem in elems:
        linked_file = elem.find_elements_by_tag_name('a')
        if len(linked_file) != 0:
            for file in linked_file:
                actions = ActionChains(browser)
                #download
                actions.move_to_element(file).perform()
                actions.click(file).perform()
                print("  Successfully download", file.text)
                counter = counter + 1
        #test sample, download 10 once

for elem in elems:
    #The start of everything here.
    #The first element for everything.
    array_for_everything = []
    name = ""
    b_tag = elem.find_elements_by_tag_name("b")
    if(len(b_tag)>0):
            #append name inside.
            nameHTML = b_tag[0].get_attribute("innerHTML")
            name = " ".join(nameHTML.split())

    #For dividing parts
    #array_for_everything.append('')
    #all possible events listed here.
    #Extracting the details of events.
    li_tag = elem.find_elements_by_tag_name("li")
        #Extracting all events
    if(len(li_tag)>0):
            for ki in range(0,len(li_tag)):
                each_action = li_tag[ki].get_attribute("innerHTML")
                #print(each_action)
                array_for_everything.append(name)
                each_action_separated = each_action.split('</b>')
                date_of_action = each_action_separated[1].split('<br>')[0][1:]
                type_of_action = each_action_separated[2].split('<br>')[0][1:]
                summary_of_action = each_action_separated[3].split('<br>')[0][1:].replace("\n", "")
                html_of_pdf = ""
                if "<a href=" in each_action_separated[3]:
                    html_of_pdf = each_action_separated[3].split('<a href=')[1].split('>')[0].replace("\"","")[1:]
                array_for_everything.append(date_of_action)
                array_for_everything.append(type_of_action)
                array_for_everything.append(summary_of_action)
                array_for_everything.append(html_of_pdf)
                array_for_everything_container.append(array_for_everything)
                #print(array_for_everything)
                array_for_everything = []
a_tags = elem.find_elements_by_tag_name("a")





    






array_for_everything_container.insert(0,['name','date of action','type of action','summary of action','html_code'])
print("Completed")
with open('attorney_with_cases.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(array_for_everything_container)

    #print(array_for_everything)
    bar.next()
    bar.next()
    bar.next()
    bar.next()
    bar.finish()

