"""
Check if every police station has uploaded at least one FIR/3months.
Draw the list of police stations who have not done so.
"""

import os
import time
from sys import argv
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# constants
# define download directory
base_directory = r'/home/sangharsh/Documents/PoA/data/FIR/check_records'
download_directory = os.path.join(base_directory, f'{argv[1]} _ {argv[2]}')
main_url = r'https://citizen.mahapolice.gov.in/Citizen/MH/PublishedFIRs.aspx'
# trying with firefox
profile = webdriver.FirefoxProfile()
# set profile for saving directly without pop-up ref -
# https://stackoverflow.com/a/29777967
profile.set_preference("browser.download.panel.shown", False)
profile.set_preference("browser.download.manager.showWhenStarting", False)
# profile.set_preference("browser.helperApps.neverAsk.openFile","application/pdf")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.dir", download_directory)
# to go undetected
profile.set_preference("general.useragent.override",
                       "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:82.0) "
                       "Gecko/20100101 Firefox/82.0")
profile.set_preference("dom.webdriver.enabled", False)
profile.set_preference('useAutomationExtension', False)
profile.set_preference("pdfjs.disabled", True)
profile.update_preferences()
# constants
driver = webdriver.Firefox(firefox_profile=profile)

# list for number of PoA FIRs & non PoA

# list of districts
ALL_Districts = ['AHMEDNAGAR', 'AKOLA', 'AMRAVATI CITY', 'AMRAVATI RURAL', 'AURANGABAD CITY',
                 'AURANGABAD RURAL', 'BEED', 'BHANDARA', 'BRIHAN MUMBAI CITY', 'BULDHANA',
                 'CHANDRAPUR', 'DHULE', 'GADCHIROLI', 'GONDIA', 'HINGOLI', 'JALGAON', 'JALNA',
                 'KOLHAPUR', 'LATUR', 'NAGPUR CITY', 'NAGPUR RURAL', 'NANDED', 'NANDURBAR',
                 'NASHIK CITY', 'NASHIK RURAL', 'NAVI MUMBAI', 'OSMANABAD', 'PALGHAR', 'PARBHANI',
                 'PIMPRI-CHINCHWAD', 'PUNE CITY', 'PUNE RURAL', 'RAIGAD', 'RAILWAY AURANGABAD',
                 'RAILWAY MUMBAI', 'RAILWAY NAGPUR', 'RAILWAY PUNE', 'RATNAGIRI', 'SANGLI', 'SATARA',
                 'SINDHUDURG', 'SOLAPUR CITY', 'SOLAPUR RURAL', 'THANE CITY', 'THANE RURAL', 'WARDHA',
                 'WASHIM', 'YAVATMAL']


# functions
# 1. open url

def open_page():
    """
    open page and refresh it. without refreshing it dose not work
    """
    driver.get(main_url)
    driver.refresh()


""" 
2. function for date to-from. same as in only details of one data will be collected.
this function needs ActionChains otherwise the dates are not getting entered. 
date will be entered through command line
"""


def enter_date(date1, date2):
    WebDriverWait(driver, 160).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ContentPlaceHolder1_txtDateOfRegistrationFrom')))
    from_date_field = driver.find_element_by_css_selector(
        '#ContentPlaceHolder1_txtDateOfRegistrationFrom')

    to_date_field = driver.find_element_by_css_selector(
        '#ContentPlaceHolder1_txtDateOfRegistrationTo')

    ActionChains(driver).click(from_date_field).send_keys(
        date1).move_to_element(to_date_field).click().send_keys(
        date2).perform()


# 3 select district and enter
def district_selection(dist_name):
    dist_list = Select(driver.find_element_by_css_selector(
        "#ContentPlaceHolder1_ddlDistrict"))

    dist_list.select_by_visible_text(dist_name)
    time.sleep(3)


# 4. List police station
def police_stations():
    WebDriverWait(driver, 160).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ContentPlaceHolder1_ddlPoliceStation')))
    select_box = driver.find_element_by_css_selector("#ContentPlaceHolder1_ddlPoliceStation")
    all_police_stations = [x.text for x in select_box.find_elements_by_tag_name("option") if x.text != "Select"]
    return all_police_stations


# 6. main code
all_the_police_stations_in_dist = {}
for name in ALL_Districts:
    driver = webdriver.Firefox(firefox_profile=profile)
    open_page()

    # call function for entering date, set the date through command line
    enter_date(date1=argv[1], date2=argv[2])

    district_selection(name)

    names_police = police_stations()

    all_the_police_stations_in_dist[name] = names_police

    driver.close()
df = pd.DataFrame(
    { key:pd.Series(value) for key, value in all_the_police_stations_in_dist.items() })


df.to_csv(os.path.join(
    base_directory, f'district_police_stations.csv'))

