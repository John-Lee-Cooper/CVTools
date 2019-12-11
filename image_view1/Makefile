run:.venv
	source .venv/bin/activate; \
	./iview.py

.venv:
	virtualenv -p python3 .venv; \
	source .venv/bin/activate; \
	pip install -r requirements.txt

clean:
	rm -rf .venv
	rm -rf __pycache__
