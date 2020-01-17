from celery import Celery
from portal.config import BaseConfig


celery = Celery(
    'Genvasc Portal',
    broker=BaseConfig.broker_url,
    backend=BaseConfig.result_backend,
)


def init_celery(app):
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        rate_limit = app.config['CELERY_RATE_LIMIT']
        
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
