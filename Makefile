DC = docker-compose
DC_FILE = infra/docker-compose.yml
DC_DEV_FILE = infra/docker-compose-dev.yml
UP_PARAMS = up -d --build rabbit notifications-admin
LOG_PARAMS = logs -f

.PHONY: up
up:
	$(DC) -f $(DC_FILE) $(UP_PARAMS)

.PHONY: down
down:
	$(DC) -f $(DC_FILE) down -v


.PHONY: logs
logs:
	$(DC) -f $(DC_FILE) $(LOG_PARAMS)

## Development
.PHONY: up-dev
up-dev:
	$(DC) -f $(DC_DEV_FILE) $(UP_PARAMS)

.PHONY: down-dev
down-dev:
	$(DC) -f $(DC_DEV_FILE) down


.PHONY: logs-dev
logs-dev:
	$(DC) -f $(DC_DEV_FILE) $(LOG_PARAMS)

