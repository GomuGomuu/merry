ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
DOCKER_COMPOSE_FILE:=$(ROOT_DIR)/docker-compose.yml

help: ## Show this help
	@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

up:  ## Start all or c=<name> containers in foreground
	@docker compose -f $(DOCKER_COMPOSE_FILE) up $(c)


down: ## Stop all or c=<name> containers
	@docker compose -f $(DOCKER_COMPOSE_FILE) down $(c)


restart: ## Restart all or c=<name> containers
	@docker compose -f $(DOCKER_COMPOSE_FILE) restart $(c)


build: ## Build all or c=<name> containers
	@docker compose -f $(DOCKER_COMPOSE_FILE) build $(c)

list-services: ## List all services
	@docker compose -f $(DOCKER_COMPOSE_FILE) config --services

join: ## Join to container c=<name>
	@docker exec -it $(c) bash