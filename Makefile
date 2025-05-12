help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-21s\033[0m %s\n", $$1, $$2}'

setup-venv: ## Setup a local venv
	python3 -m venv venv

install-deps: ## Install python dependencies for development
	pip install -r requirements.txt -r requirements-dev.txt

UVICORN_COMMON_OPTS = better_whoami.app:app \
		--host ::  \
		--port 8000 \
		--no-server-header

start: ## Start a production like server
	poetry run uvicorn $(UVICORN_COMMON_OPTS)

dev: ## Start the local development server
	poetry run uvicorn $(UVICORN_COMMON_OPTS) \
		--reload \
		--log-level debug

lint: ## Lint the code according to the standards
	poetry run ruff check .
	poetry run ruff format --check .
	poetry run pyright .

format: ## Format the code according to the standards
	poetry run ruff check --fix .
	poetry run ruff format .
