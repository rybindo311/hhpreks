import os

from dotenv import load_dotenv


load_dotenv()  # загружает переменные из .env


SEARCH = os.getenv("SEARCH", "python-developer")
WORK_FORMAT = os.getenv("WORK_FORMAT", "REMOTE")
VACANCY_HTML = os.getenv("VACANCY_HTML", "temp/vacancies.html")
PARSED = os.getenv("PARSED", "temp/parsed")
CHROME_BINARY = os.getenv("CHROME_BINARY", "/usr/bin/google-chrome")
APPLIED = os.getenv("APPLIED", "applied.json")