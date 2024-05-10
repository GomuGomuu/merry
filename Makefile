ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER_COMPOSE_FILE:=$(ROOT_DIR)/docker-compose.yml

help: ## Show this help
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

docker-up:  ## Start all or c=<name> containers in foreground
	@docker compose -f $(DOCKER_COMPOSE_FILE) up $(c)


docker-down: ## Stop all or c=<name> containers
	@docker compose -f $(DOCKER_COMPOSE_FILE) down $(c)


docker-restart: ## Restart all or c=<name> containers
	@docker compose -f $(DOCKER_COMPOSE_FILE) restart $(c)


docker-build: ## Build all or c=<name> containers
	@docker compose -f $(DOCKER_COMPOSE_FILE) build $(c)

docker-list-services: ## List all services
	@docker compose -f $(DOCKER_COMPOSE_FILE) config --services

docker-join: ## Join to container c=<name>
	@docker exec -it $(c) bash

resetdatabase:
	docker exec -it merry-postgres psql -p 5432 -U postgres -d postgres -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
	python src/manage.py migrate
	python src/manage.py init_base

start: # Up django
	@docker compose up -d merry-postgres
	@timeout 5
	python src/manage.py runserver 0.0.0.0:8000