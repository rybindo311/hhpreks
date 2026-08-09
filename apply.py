from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROME_BINARY = "/usr/bin/chromium"

def start_browser_and_wait_for_login():
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY
    chrome_options.add_argument("--start-maximized")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://spb.hh.ru/")
    input("login and press Enter")
    return driver
 
def main():
    driver = start_browser_and_wait_for_login()

    with open("parsed", "r") as f:
        ids = f.readlines()
        ids = ids[::-1]

    for id in ids:
        link = f"https://spb.hh.ru/applicant/vacancy_response?vacancyId={id}&hhtmFrom=vacancy"
        driver.get(link)
        print(f"applied on id {id}")
        sleep(2)

if __name__ == "__main__":
    main()
