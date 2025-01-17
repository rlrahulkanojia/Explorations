export PYTHONPATH := .:$(CODE):$(PYTHONPATH)

CODE=service
UNIT_TESTS=tests
POETRY_ARG=poetry run

static-tests:
	###### Running linter analysis ######
	$(POETRY_ARG) ruff check $(CODE)

unit-tests:
	###### Running unit tests ######
	$(POETRY_ARG) pytest -vv $(UNIT_TESTS)

all: static-tests unit-tests


docker-build:
	###### Docker build the API service ######
	DOCKER_BUILDKIT=1 docker build --rm  --tag api:dev .

docker-run:
	###### Docker run the API service ######
	docker run -it --name api-dev -p 8080:8080 --rm api:dev $(RUN_DOCKER)

api:
	###### Run the API service development mode ######
	$(POETRY_ARG) uvicorn service.main:app --log-level info --host 0.0.0.0 --port 8080 --reload --reload-dir service

run-streamlit:
	$(POETRY_ARG) streamlit run streamlit/streamlit.py