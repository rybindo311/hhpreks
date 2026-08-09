#!/bin/bash

TEXT="python-developer"

OUTPUT="temp/vacancies.html"
> "$OUTPUT"

for PAGE in {0..10}; do
  echo "Скачиваю страницу $PAGE..."
  curl -s -L \
    -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    "https://hh.ru/search/vacancy?text=$TEXT&salary=&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&items_on_page=100&page=$PAGE" >> "$OUTPUT"
  echo -e "\n\n<!-- Конец страницы $PAGE -->\n\n" >> "$OUTPUT"
  sleep 1
done

echo "Готово! Все страницы сохранены в $OUTPUT"

