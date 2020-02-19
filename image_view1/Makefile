SHELL := /bin/bash

run:.venv
	source .venv/bin/activate; \
	./iview.py

.venv:requirements
	make clean; \
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip install -r requirements
	pip freeze > requirements.txt

clean:
	rm -rf .venv
	rm -rf __pycache__
	rm requirements.txt
