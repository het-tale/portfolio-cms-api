DB_MESSAGE ?= "auto migration"

migrate:
	alembic revision --autogenerate -m "$(DB_MESSAGE)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1
