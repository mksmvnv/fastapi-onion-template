.PHONY: all run lint format install
.SILENT: all run lint format install

ABS := $(shell pwd)
SRC := $(ABS)/backend

all: format lint run

run:
	poetry run python3 $(SRC)/main.py

lint:
	poetry run flake8 $(SRC)
	poetry run mypy $(SRC)

format:
	poetry run black $(SRC)

install:
	poetry install