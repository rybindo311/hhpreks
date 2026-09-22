import re
import json

from conf import VACANCY_HTML, PARSED

def extract_matching_refs(file_path):
    pattern = re.compile(r"https://(?:[a-zA-Z0-9-]+\.)?hh\.(?:ru|kz|by|uz|am|az|ge|kg|tj|tm)/vacancy/(\d+)")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    ids = set(pattern.findall(text))

    return ids


def main():
    file_path = VACANCY_HTML
    output_path = PARSED
    refs = extract_matching_refs(file_path)
    print(f"Нашлось {len(refs)} вакансий")
    with open(output_path, "w") as f:
        json.dump([int(ref) for ref in refs], f)

if __name__ == "__main__":
    print("Начало парсинга.")
    main()
    print("парсинг завершён.")
