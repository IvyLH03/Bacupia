celery:
	celery -A tasks worker --loglevel=INFO

flask:
	flask --app api run

gunicorn:
	gunicorn -w 4 'api:app' -b 127.0.0.1:5000