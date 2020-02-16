SHELL := /bin/bash

run:.venv
	source .venv/bin/activate; \
	./iview.py

.venv:requirements
	make clean; \
	virtualenv -p python3 .venv; \
	source .venv/bin/activate; \
	pip install -r requirements
	pip freeze > requirements.txt

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm requirements.txt
