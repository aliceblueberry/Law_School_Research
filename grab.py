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
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(executable_path = "./chromedriver", chrome_options=options);
# The website we wish to retrieve information from.
browser.get("https://www.dcbar.org/attorney-discipline/disciplinary-decisions.cfm");
try:
    print("Waiting the Page to load");
    element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "startDate"))
    )
finally:
    print("Page loaded");
    date_from = browser.find_element(By.ID, "startDate");
    print(date_from);
    #Wait for the thing to load fully. You can tweak it if you like.
    #First Step: Extract everything, and throw them in a CSV file.
    time.sleep(3);
    date_from.click();
    date_from.clear();
    date_from.send_keys("2019/01/01");
    date_from.send_keys(Keys.ENTER);
    time.sleep(2);
    elems = browser.find_elements(By.XPATH, '//form')
    print(len(elems))
    #Now put everything here into CSV. But now, try to store them.
    array_for_everything_container = []
    all_the_links = []
    #in-var
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
                array_for_everything.append(date_of_action)
                array_for_everything.append(type_of_action)
                array_for_everything.append(summary_of_action)
                array_for_everything_container.append(array_for_everything)
                print(array_for_everything)
                array_for_everything = []
        a_tags = elem.find_elements_by_tag_name("a")
        if(len(a_tags)>0):
            for ki in a_tags:
                all_the_links.append(ki.get_attribute("href"))
                #print(ki.get_attribute("href"))
    array_for_everything_container.insert(0,['name','date of action','type of action','summary of action'])
    with open('protagonist.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(array_for_everything_container)
        #print(array_for_everything)
