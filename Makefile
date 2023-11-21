SHELL := /bin/bash

COMPOSE_PATH=bin/docker/docker-compose.yml

RUN_COMPOSE_TEST=docker-compose -f $(COMPOSE_PATH) \
		--profile=test up --build -d ; docker-compose -f $(COMPOSE_PATH) logs tests -f

RUN_COMPOSE_ENV=docker-compose -f $(COMPOSE_PATH) up -d --build


setup:
	./bin/scripts/setup_env.sh
test:
	@${RUN_COMPOSE_TEST}
env:
	@$(RUN_COMPOSE_ENV)
format:
	@$(RUN) ./bin/scripts/format.sh
lint:
	@$(RUN) ./bin/scripts/lint.sh
build:
	docker build . -t kassett-actions
