all: deps static

deps:
	npm install

static:
	webpack

watch:
	webpack --watch


run:
	python app.py


web:
	gunicorn --preload --keep-alive=10 --debug --workers 4 --bind 0.0.0.0:5000 --worker-class socketio.sgunicorn.NginxGeventSocketIOWorker app:web
