#!/usr/bin/make

include .env

SHELL = /bin/sh
CURRENT_UID := $(shell id -u):$(shell id -g)

export CURRENT_UID

up:
	DEBUGPY=False docker-compose up -d --force-recreate --build --remove-orphans
upd:
	DEBUGPY=True docker-compose up -d  --build
down:
	DEBUGPY=True docker-compose down
sh:
	docker exec -it /nav_backend /bin/sh
migrations:
	docker exec -it /nav_backend python3 manage.py makemigrations
su:
	docker exec -it /nav_backend python3 manage.py createsuperuser
logs:
	docker logs /nav_backend -f