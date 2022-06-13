SHELL := /bin/bash

export PYTHONPATH=$(shell pwd)

setup:
	poetry install

test: tests

tests::
	poetry run pytest tests -v \
		--cov=pipdev \
		--disable-warnings \
		--cov-report html \
		--cov-report term \
		-p no:doctest

build:
	poetry build
