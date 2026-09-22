#!/bin/bash

source .env

export WORK_FORMAT
export VACANCY_HTML
> "$VACANCY_HTML"

# тот же паттерн ссылок на вакансию, что использует parse.py —
# по нему определяем, есть ли на странице хоть одна вакансия
VACANCY_LINK_PATTERN='https://[a-zA-Z.]+hh\.ru/vacancy/[0-9]+'

# несколько поисковых запросов в SEARCH перечисляются через запятую,
# например: SEARCH="developer+fastapi,python-developer"
IFS=',' read -ra QUERIES <<< "$SEARCH"

for QUERY in "${QUERIES[@]}"; do
  echo "Запрос: $QUERY"

  for PAGE in {0..10}; do
    echo "Скачиваю страницу $PAGE..."
    PAGE_HTML=$(curl -s -L \
      -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36" \
      -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
      "https://hh.ru/search/vacancy?text=$QUERY&salary=&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&items_on_page=100&page=$PAGE&work_format=$WORK_FORMAT")

    if ! grep -qE "$VACANCY_LINK_PATTERN" <<< "$PAGE_HTML"; then
      echo "Страница $PAGE не содержит вакансий — останавливаю скачивание для запроса \"$QUERY\"."
      break
    fi

    echo "$PAGE_HTML" >> "$VACANCY_HTML"
    echo -e "\n\n<!-- Конец страницы $PAGE (запрос: $QUERY) -->\n\n" >> "$VACANCY_HTML"
    sleep 1
  done
done

echo "Готово! Все страницы сохранены в $VACANCY_HTML"

