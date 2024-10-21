#!/bin/sh

## Установить PYTHONPATH, чтобы указать Python, где искать модули
export PYTHONPATH=$(pwd)

## Запуск бота телеграмма
python app/main.py &

### Celery
#celery -A app.celery_settings.main worker -Q arbitration_main -c 1 -l INFO -n arbitration@%h &
#
## Для переодических задач
#celery -A app.celery_settings.main beat -l INFO -s /tmp/celerybeat-schedule