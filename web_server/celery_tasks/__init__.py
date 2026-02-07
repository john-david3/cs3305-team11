"""Celery configuration and Flask app context setup for async tasks."""

from celery import Celery, Task


def celery_init_app(app) -> Celery:
    """Initialize Celery with Flask application context."""
    class FlaskTask(Task):
        """Celery task that runs within Flask app context."""
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.conf.beat_schedule = {
        'user-favourability-task': {
            'task': 'celery_tasks.preferences.user_preferences',
            'schedule': 30.0,
        },
    }
    celery_app.conf.include = [
        'celery_tasks.preferences',
        'celery_tasks.streaming',
    ]
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
