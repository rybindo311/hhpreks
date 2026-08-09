
import re

def extract_matching_refs(file_path):
    pattern = re.compile(r"https://hh\.ru/vacancy/(\d+)")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    ids = set(pattern.findall(text))

    return ids


def main():
    file_path = "temp/vacancies.html"
    output_path = "temp/parsed"
    refs = extract_matching_refs(file_path)
    with open(output_path, "w") as f:
        f.writelines(ref + '\n' for ref in refs)

if __name__ == "__main__":
    main()
