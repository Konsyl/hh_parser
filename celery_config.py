CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
REDIS_CONNECT_RETRY = True
CELERY_SEND_EVENTS = True

#CELERY_RESULT_BACKEND = 'redis'
#CELERYBEAT_SCHEDULER="djcelery.schedulers.DatabaseScheduler"
