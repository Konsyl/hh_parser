from celery import Celery
from datetime import timedelta

app = Celery('proj')
app.config_from_object('hh_parser.celery_config', namespace='CELERY')


app.conf.beat_schedule = {
    'parsing': {
        'task': 'hh_parser.tasks.start_parsing',
        'schedule': timedelta(hours=4)
    },

    'status': {
        'task': 'hh_parser.tasks.start_status',
        'schedule': timedelta(hours=2)

    }
}

# FILE IN WORKING