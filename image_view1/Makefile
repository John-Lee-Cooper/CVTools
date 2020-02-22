SHELL := /bin/bash

run:.venv
	source .venv/bin/activate; \
	./iview.py

clean:
	-@rm -f requirements.txt
	-@rm -rf .venv
	-@rm -rf __pycache__
	-@rm -rf build dist *.spec

.venv:requirements
	make clean; \
	python3 -m venv .venv; \
	source .venv/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements;
	pip freeze > requirements.txt;

exe:.venv
	pyinstaller --windowed iview2
	#pyinstaller --hidden-import freetype-py iview2.py
	-@cp -r .venv/lib/python3.8/site-packages/freetype dist/iview2
	-@rm -f ~/bin/iview
	ln -s ~/python/cv_tools/image_view1/dist/iview2/iview2 ~/bin/iview
	~/bin/iview --help > /dev/null
	#ln -s $(cd dist/iview2/ && pwd -P)/iview2 ~/bin/iview
