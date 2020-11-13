"""
the file was running fine at per_day_FIRs.py
one day per district covering all district units
now this file aims to open a new instance everytime it changes the district
this is quite essential as it has been observed that
due portal failure, the page stops behaving properly and keeps
showing the old data.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
from sys import argv
import os
from data_summary import poa_district_summary

# constants
# define download directory
base_directory = r'/home/sangharsh/Documents/data/FIR_Data'
download_directory = os.path.join(base_directory, f'{argv[1]}')
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
non_PoA = []
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


# 2 select district and enter
def district_selection(dist_name):
    dist_list = Select(driver.find_element_by_css_selector(
        "#ContentPlaceHolder1_ddlDistrict"))

    # command line input
    dist_list.select_by_visible_text(dist_name)
    time.sleep(6)


""" 
2. function for date to-from. same as in only details of one data will be collected.
this function needs ActionChains otherwise the dates are not getting entered. 
date will be entered through command line
"""


def enter_date(date):
    WebDriverWait(driver, 160).until(
        ec.presence_of_element_located((By.CSS_SELECTOR,
                                        '#ContentPlaceHolder1_txtDateOfRegistrationFrom')))
    from_date_field = driver.find_element_by_css_selector(
        '#ContentPlaceHolder1_txtDateOfRegistrationFrom')

    to_date_field = driver.find_element_by_css_selector(
        '#ContentPlaceHolder1_txtDateOfRegistrationTo')

    ActionChains(driver).click(from_date_field).send_keys(
        date).move_to_element(to_date_field).click().send_keys(
        date).perform()


# 3. view 50 records at a time
def view_record():
    view = Select(driver.find_element_by_id('ContentPlaceHolder1_ucRecordView_ddlPageSize'))
    view.select_by_value("50")


# 4. function for click on search
def search():
    driver.find_element_by_css_selector('#ContentPlaceHolder1_btnSearch').click()
    time.sleep(5)


# 5 check if it has PoA if yes, create a list of how many cases
def check_the_act(some_list):
    # check for PoA in table.
    # identify table first
    try:
        WebDriverWait(driver, 10).until(

            ec.presence_of_element_located((By.CSS_SELECTOR, "#ContentPlaceHolder1_gdvDeadBody")))
    except NoSuchElementException:
        return print("no PoA")
    table = driver.find_element(By.ID, "ContentPlaceHolder1_gdvDeadBody")
    rows = table.find_elements(By.TAG_NAME, "tr")
    # iterate over each row
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        # iterate over each cell
        for cell in cells:
            cell_text = cell.text
            # if the act is found, count it. and take details.
            if "अनुसूचीत जाती आणि अनुसूचीत" in cell_text:
                some_list.append(row.text)
            else:
                non_PoA.append(row.text)


def download_repeat(date, district, some_list):
    i = 0
    while i <= len(some_list) - 1:
        open_page()
        time.sleep(1)
        enter_date(date)
        district_selection(district)
        view_record()
        search()
        time.sleep(2)
        table = driver.find_element(By.ID, "ContentPlaceHolder1_gdvDeadBody")
        rows = table.find_elements(By.TAG_NAME, "tr")
        main_window = driver.current_window_handle
        new_list = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            # iterate over each cell
            for cell in cells:
                cell_text = cell.text
                # if the act is found, count it. and take details.
                if "अनुसूचीत जाती आणि अनुसूचीत" in cell_text:
                    download_link = row.find_element(By.TAG_NAME, "input")
                    new_list.append(download_link)
                else:
                    continue
        new_list[i].click()
        for handle in driver.window_handles:
            if handle != main_window:
                download_window = handle
                # we are in main window, so go to next window
                driver.switch_to.window(download_window)

                time.sleep(4)

                driver.find_element_by_id(
                    "ReportViewer1_ctl06_ctl04_ctl00_ButtonImgDown").click()
                down_load = driver.find_element_by_css_selector(
                    "#ReportViewer1_ctl06_ctl04_ctl00_Menu > div:nth-child(4) > a:nth-child(1)"
                )
                print(down_load.text)
                down_load.send_keys(Keys.ENTER)
                time.sleep(2)
                driver.close()
                driver.switch_to.window(main_window)
        i += 1


# 6. main code


for name in ALL_Districts:
    driver = webdriver.Firefox(firefox_profile=profile)
    open_page()

    # call function for entering date, set the date through command line
    enter_date(date=argv[1])
    poa_cases = []
    # call function district, for now its Dhule. will change latter to command line
    district_selection(name)
    # call the value of records to view @ 50
    view_record()
    # call search
    search()
    # wait for 5 sec
    # time.sleep(5)
    # call function check the act and click download

    check_the_act(some_list=poa_cases)
    if not poa_cases:
        print(f"no PoA case {name}")
    else:
        poa_district_summary(poa_cases, name, argv[1])
        download_repeat(argv[1], name, poa_cases)
    driver.close()
