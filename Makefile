install:
	poetry lock --no-update
	poetry install --no-root --no-interaction --with=dev,test

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -f poetry.lock

format:
	poetry run black .

build: clean install
	poetry build

all: clean install build