ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER_COMPOSE_FILE:=$(ROOT_DIR)/docker-compose.yml

help: ## Show this help
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

docker-up:
	@docker compose up


docker-down:
	@docker compose down


docker-restart:
	@docker compose restart


docker-build:
	@docker compose build

docker-list-services:
	@docker compose config --services

docker-join: ## Join to container c=<name>
	@docker exec -it $(c) bash

start: # Up django
	@docker compose up -d merry-postgres
	@timeout 5
	python src/manage.py runserver 0.0.0.0:8000