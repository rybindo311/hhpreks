import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)

from conf import CHROME_BINARY, PARSED, APPLIED, COVER_LETTER

PAGE_LOAD_TIMEOUT = 15  # секунд, после чего перестаём ждать полную загрузку страницы
SUBMIT_BUTTON_SELECTOR = "button[data-qa='vacancy-response-submit-popup']"
LETTER_FIELD_SELECTOR = "textarea[data-qa='vacancy-response-popup-form-letter-input']"

# фразы, которыми hh.ru сообщает об ошибке отклика (берутся из видимого текста
# страницы после клика — не из вёрстки/атрибутов, которые могут поменяться)
RESPONSE_ERROR_MARKERS = (
    "введите сопроводительное письмо",
    "ответить на вопросы теста",
    "уже откликались на эту вакансию",
    "недопустимое сообщение",
    "нарушает правила сервиса",
    "уберите нецензурные слова",
    "произошла ошибка, попробуйте ещё раз",
    "сайт перегружен",
    "не более 200 откликов",
    "измените видимость резюме",
    "невозможно откликнуться",
)
RESPONSE_SUCCESS_MARKERS = (
    "отклик отправлен",
    "резюме доставлено",
)


def fill_cover_letter(driver):
    if not COVER_LETTER:
        return
    fields = driver.find_elements(By.CSS_SELECTOR, LETTER_FIELD_SELECTOR)
    if not fields:
        return  # для этой вакансии сопроводительное письмо не запрашивается
    letter_field = fields[0]
    if letter_field.get_attribute("value"):
        return  # уже что-то заполнено — не перетираем
    letter_field.send_keys(COVER_LETTER)


def submit_response(driver):
    """Пытается отправить отклик. Возвращает (True, None) при успехе,
    иначе (False, причина) — причина берётся из текста, который сайт
    показал в ответ на попытку отклика, а не из атрибутов вёрстки."""
    try:
        button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, SUBMIT_BUTTON_SELECTOR)))
    except TimeoutException:
        return False, "кнопка отклика не найдена на странице"

    fill_cover_letter(driver)

    try:
        button.click()
    except (ElementClickInterceptedException, ElementNotInteractableException):
        return False, "кнопка отклика неактивна (форма не заполнена)"

    try:
        WebDriverWait(driver, 5).until(EC.staleness_of(button))
        return True, None
    except TimeoutException:
        pass  # форма осталась на странице — смотрим, что сайт написал в ответ

    try:
        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
    except StaleElementReferenceException:
        return True, None  # страница успела смениться прямо во время чтения

    for marker in RESPONSE_SUCCESS_MARKERS:
        if marker in body_text:
            return True, None

    for marker in RESPONSE_ERROR_MARKERS:
        if marker in body_text:
            return False, marker

    return False, "отклик не отправлен (форма осталась на странице)"


def start_browser_and_wait_for_login():
    chrome_options = Options()
    chrome_options.binary_location = CHROME_BINARY
    chrome_options.add_argument("--start-maximized")
    # снижаем узнаваемость автоматизации — иначе антибот hh.ru может
    # держать сессию на бесконечном экране проверки
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    # не ждём полной догрузки всех ресурсов (трекеры/аналитика) —
    # достаточно того, что DOM готов к взаимодействию
    chrome_options.page_load_strategy = "eager"

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    driver.get("https://hh.ru/")
    input("Войдите в акаунт и нажмите любую кнопку.")
    return driver


def save_applied(applied_ids):
    with open(APPLIED, "w", encoding="utf-8") as f:
        json.dump(applied_ids, f, ensure_ascii=False, indent=4)


def main():
    driver = start_browser_and_wait_for_login()

    with open(PARSED, "r") as f:
        ids = json.load(f)
        ids = ids[::-1]

    counter = 0

    with open(APPLIED, "r", encoding="utf-8") as file:
        applied_ids = json.load(file)

    try:
        for i, id in enumerate(ids):

            if id in applied_ids:
                print(f"{i}. Вакансия {id=} обработана ранее")
                continue

            link = f"https://hh.ru/applicant/vacancy_response?vacancyId={id}&hhtmFrom=vacancy"

            try:
                driver.get(link)
            except TimeoutException:
                # страница не догрузилась за отведённое время — останавливаем
                # загрузку и пробуем работать с тем, что уже успело отрисоваться
                driver.execute_script("window.stop();")

            sleep(2)
            try:
                applied, reason = submit_response(driver)
            except WebDriverException as e:
                applied, reason = False, f"ошибка браузера: {e}"

            if applied:
                print(f"{i}. Обработана вакансия {id=}")
                counter += 1
                applied_ids.append(int(id))
                save_applied(applied_ids)
            else:
                print(f"{i}. Вакансия {id=} пропущена ({reason})")

            sleep(2)

            if counter == 150:
                break
    finally:
        save_applied(applied_ids)

    print(f"Скрипт завершил работу. Обработано {counter} вакансий")

if __name__ == "__main__":
    print("Автоотклик запущен.")
    main()
    print("Автоотклик завершил работу.")
