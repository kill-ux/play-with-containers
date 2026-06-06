ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)

up:
	docker compose up --build $(ARGS)

stop:
	docker compose stop

down:
	docker compose down

clean:
	docker compose down -v

re: clean up

prune:
	docker image prune -a


.PHONY: up stop clean re prune