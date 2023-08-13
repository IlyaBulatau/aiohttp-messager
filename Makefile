start:
	docker compose up -d --build && docker logs aiohttp-messager-app-1 --follow
stop:
	docker compose down -v
relogs:
	docker logs aiohttp-messager-app-1 --follow
psql:
	docker exec -it --user postgres aiohttp-messager-db-1 psql 