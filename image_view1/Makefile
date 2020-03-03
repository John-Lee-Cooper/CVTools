SHELL := /bin/bash

run:venv
	source venv/bin/activate; \
	./iview.py

clean:
	-@rm -f requirements.txt
	-@rm -rf venv
	-@rm -rf __pycache__
	#-@rm -rf build dist *.spec
	-@rm -rf build dist setup.py
	-@rm -f .DS_Store ../.DS_Store

venv:requirements
	make clean; \
	python3 -m venv venv; \
	source venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements;
	pip freeze > requirements.txt;

exe:venv
	-@rm -rf build dist setup.py
	py2applet --make-setup i_view.py
	python setup.py py2app -A --argv-emulation --emulate-shell-environment
	-@rm -rf ~/Applications/i_view.app
	mv dist/i_view.app ~/Applications
	-@rm -rf build dist setup.py

