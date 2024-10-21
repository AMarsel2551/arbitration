import asyncio, traceback
from celery import Celery
from kombu import Queue
from app.celery_settings.functional import cleaning_at_start, get_interval_hours_minutes, clear_quene
from app.settings import com_settings, redis_settings
from app.logger import log
from celery.exceptions import SoftTimeLimitExceeded
from app.scraping.main import main as scraping_currency_main


celery_app = Celery(
   com_settings.APPLICATION_NAME,
    broker=f"redis://{redis_settings.login}:{redis_settings.password}@{redis_settings.ip_address}:{redis_settings.port}",
    backend=f'redis://{redis_settings.login}:{redis_settings.password}@{redis_settings.ip_address}:{redis_settings.port}',
    broker_connection_retry_on_startup=True
)


celery_app.conf.timezone = 'Europe/Moscow'
celery_app.conf.enable_utc = False

# Обьявление очередей
celery_app.conf.task_queues = (
    Queue(name='arbitration_main'),
)


# Чистка очередей перед запуском
cleaning_at_start(celery_app=celery_app)


# celery_app.conf.beat_schedule = {
#     'scraping_currency': {
#         'task': "scraping_currency",
#         'schedule': get_interval_hours_minutes(1),
#     },
# }


@celery_app.task(name="scraping_currency", queue="arbitration_main", soft_time_limit=60*10)
def cscraping_cards():
    try:
        clear_quene(celery_app=celery_app, queue_name="arbitration_main")
        loop = asyncio.new_event_loop()
        loop.run_until_complete(scraping_currency_main())

    except SoftTimeLimitExceeded as e:
        return {'status': 'TimeLimit', 'error': f'{e}'}

    except:
        log.error(f"{traceback.format_exc()}")
        return {'status': 'error', 'error': f'{traceback.format_exc()}'}