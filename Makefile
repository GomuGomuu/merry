ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER_COMPOSE_FILE:=$(ROOT_DIR)/docker-compose.yml

help: ## Show this help
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

restart:
	@docker compose restart

build:
	@docker compose build

docker-list-services:
	@docker compose config --services

docker-join: ## Join to container c=<name>
	@docker exec -it $(c) bash

up: # Up django
	@docker compose up

down: # Down django
	@docker compose down