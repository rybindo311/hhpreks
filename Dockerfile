FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Chromium + chromedriver одной версии из Debian; Xvfb/x11vnc/noVNC нужны, чтобы
# войти в аккаунт hh.ru через браузер на http://localhost:6080
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium chromium-driver \
        xvfb x11vnc novnc websockify \
        curl ca-certificates fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости берём из pyproject.toml, чтобы не дублировать их списком
COPY pyproject.toml .
RUN python -c "import tomllib; print('\n'.join(tomllib.load(open('pyproject.toml', 'rb'))['project']['dependencies']))" > /tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY conf.py parse.py apply.py search.sh run.sh docker-entrypoint.sh ./
RUN mkdir -p temp && chmod +x docker-entrypoint.sh

ENV CHROME_BINARY=/usr/bin/chromium \
    CHROME_PROFILE_DIR=/data/chrome-profile \
    CHROME_EXTRA_ARGS="--no-sandbox --disable-dev-shm-usage --window-position=0,0 --window-size=1366,900" \
    VACANCY_HTML=temp/vacancies.html \
    PARSED=temp/parsed.json \
    APPLIED=applied.json

EXPOSE 6080

ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["bash", "run.sh"]
