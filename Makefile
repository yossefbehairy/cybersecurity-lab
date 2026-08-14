COMPOSE=docker compose

.PHONY: setup start stop restart status health reset test logs shell clean

setup:
	@sh scripts/setup.sh

start:
	@sh scripts/start.sh

stop:
	@sh scripts/stop.sh

restart: stop start

status:
	@$(COMPOSE) ps

health:
	@sh scripts/health-check.sh

reset:
	@sh scripts/reset.sh

test:
	@python -m pytest -q

logs:
	@$(COMPOSE) logs --tail=100 -f

shell:
	@$(COMPOSE) exec analyst-tools sh

clean:
	@$(COMPOSE) down -v --remove-orphans

