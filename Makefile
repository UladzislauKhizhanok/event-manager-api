.PHONY: $(MAKECMDGOALS)
SERVICE_NAME = web

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile \
	| awk 'BEGIN{FS=":.*## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

build: ## Build the docker image
	docker compose build

lint: ## Run linters
	pre-commit run --all-files

up: build ## Up the docker-compose
	docker compose up --remove-orphans

test: build ## Run tests
	docker compose run --rm $(SERVICE_NAME) test

down: ## Down the docker-compose
	docker compose down --remove-orphans
