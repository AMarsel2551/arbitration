from celery.schedules import crontab
from kombu import Queue


def cleaning_at_start(celery_app):
    with celery_app.connection_or_acquire() as conn:
        channel = conn.default_channel
        for quene in celery_app.conf.task_queues:
            try:
                queue = Queue(name=quene.name, channel=channel)
                queue.purge()
            except:
                pass


def clear_quene(celery_app, queue_name: str):
    with celery_app.connection_or_acquire() as conn:
        Queue(name=queue_name, channel=conn.default_channel).purge()


def get_interval_hours(interval: int):
    time =  ','.join([str(i) for i in range(0, 24, interval)])
    return crontab(hour=time, minute='00')


def get_interval_hours_minutes(interval: int):
    time = ','.join([str(i) for i in range(1, 59, interval)])
    return crontab(minute=time)