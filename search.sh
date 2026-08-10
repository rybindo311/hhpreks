#!/bin/bash

source .env

export SEARCH
export WORK_FORMAT
export VACANCY_HTML
> "$VACANCY_HTML"

for PAGE in {0..10}; do
  echo "Скачиваю страницу $PAGE..."
  curl -s -L \
    -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    "https://hh.ru/search/vacancy?text=$SEARCH&salary=&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&items_on_page=100&page=$PAGE&work_format=$WORK_FORMAT" >> "$VACANCY_HTML"
  echo -e "\n\n<!-- Конец страницы $PAGE -->\n\n" >> "$VACANCY_HTML"
  sleep 1
done

echo "Готово! Все страницы сохранены в $VACANCY_HTML"

