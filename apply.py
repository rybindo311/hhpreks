import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conf import CHROME_BINARY, PARSED, APPLIED


def start_browser_and_wait_for_login():
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://hh.ru/")
    input("Войдите в акаунт и нажмите любую кнопку.")
    return driver
 
def main():
    driver = start_browser_and_wait_for_login()

    with open(PARSED, "r") as f:
        ids = f.readlines()
        ids = ids[::-1]

    counter = 0

    with open(APPLIED, "r", encoding="utf-8") as file:
        applied_ids = json.load(file)

    for id in ids:

        if id in applied_ids:
            continue

        link = f"https://hh.ru/applicant/vacancy_response?vacancyId={id}&hhtmFrom=vacancy"
        driver.get(link)
        sleep(2)
        try:
            button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((
                    By.XPATH,
                    "//span[contains(@class, 'magritte-button__content')]/ancestor::button")))  # ждём только 3 секунды
            button.click()
            print(f"Обработана вакансия {id=}")
            counter += 1

        except:
            print(f"вакансия {id=} пропущена")

        sleep(2)

        if counter == 200:
            break

    applied_ids = applied_ids + ids

    with open(APPLIED, 'w', encoding='utf-8') as f:
        json.dump(applied_ids, f, ensure_ascii=False, indent=4)
        
    print(f"Скрипт завершил работу. Обработано {counter} вакансий")

if __name__ == "__main__":
    print("Автоотклик запущен.")
    main()
    print("Автоотклик завершил работу.")
