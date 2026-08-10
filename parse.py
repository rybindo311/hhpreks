import re

from conf import VACANCY_HTML, PARSED

def extract_matching_refs(file_path):
    pattern = re.compile(r"https://hh\.ru/vacancy/(\d+)")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    ids = set(pattern.findall(text))

    return ids


def main():
    file_path = VACANCY_HTML
    output_path = PARSED
    refs = extract_matching_refs(file_path)
    with open(output_path, "w") as f:
        f.writelines(ref + '\n' for ref in refs)

if __name__ == "__main__":
    print("Начало парсинга.")
    main()
    print("парсинг завершён.")
