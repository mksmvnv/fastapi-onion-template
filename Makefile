.PHONY: all run lint format

SRC = backend

all: format run

run:
	fastapi dev $(SRC)/main.py

lint:
	flake8 $(SRC)

format:
	autopep8 -ira $(SRC)