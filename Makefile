CURRENT_DIR := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SHELL = /bin/bash

.PHONY: help
help: ## Print available targets.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


.PHONY: build
build: ## Build the project.
	@make create-venv
	@make start-venv
	@make dependencies


.PHONY: run
run: ## Start the venv.
	@make start-venv


.PHONY: start-venv
start-venv:
	@echo "starting venv"
	@source venv/bin/activate

.PHONY: test
test: ## Run test suite.
	@python -m pytest .


.PHONY: create-venv
create-venv: ## Create and activate python venv.
	@echo "Installing venv"
	@python3 -m venv venv
	@source venv/bin/activate

.PHONY: dependencies
dependencies: ## Installing dependencies.
	@echo "Installing dependencies"
	@poetry install

.PHONY: game
game: ## Init Tibia Executable.
	@echo "Executing Tibia"
	@cd ~/Programs/Tibia; ./start-tibia-launcher.sh


