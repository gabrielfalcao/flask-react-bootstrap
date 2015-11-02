all: deps static

deps:
	npm install

static:
	webpack

watch:
	webpack --watch


run:
	python app.py

workers:
	supervisord -c supervisor.conf
