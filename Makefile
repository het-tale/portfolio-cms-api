DB_MESSAGE ?= "auto migration"

migrate:
	alembic revision --autogenerate -m "$(DB_MESSAGE)"

upgrade:
	alembic upgrade head

downgrade:
	alembic downgrade -1

up:
	bash scripts/prestart.sh && uvicorn app.main:app --reload