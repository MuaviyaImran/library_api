run:
	python run.py

install:
	pipenv install
	pipenv install --dev

clean:
	pipenv --rm