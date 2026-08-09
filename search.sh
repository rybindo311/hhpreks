#!/bin/bash

TEXT="project-manager"

OUTPUT="vacancies.html"
> "$OUTPUT"

for PAGE in {0..10}; do
  echo "Скачиваю страницу $PAGE..."
  curl -s "https://spb.hh.ru/search/vacancy?text=$TEXT&salary=&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&items_on_page=100&page=$PAGE" >> "$OUTPUT"
  echo -e "\n\n<!-- Конец страницы $PAGE -->\n\n" >> "$OUTPUT"
  sleep 1
done

echo "Готово! Все страницы сохранены в $OUTPUT"

