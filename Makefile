# Mini-CRM — project commands
# Usage: make <target>   (run `make help` for the list)

BACKEND_DIR := backend
FRONTEND_DIR := frontend
BACKEND_PORT ?= 8001
VENV := $(BACKEND_DIR)/.venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.DEFAULT_GOAL := help
.PHONY: help install install-backend install-frontend seed backend frontend dev \
        up down build logs clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ── Local development ───────────────────────────────────────────────────────

install: install-backend install-frontend ## Install backend + frontend deps

install-backend: ## Create venv and install Python deps
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r $(BACKEND_DIR)/requirements.txt

install-frontend: ## Install npm deps
	cd $(FRONTEND_DIR) && npm install

seed: ## Load initial demo data into the database
	cd $(BACKEND_DIR) && ../$(VENV)/bin/python seed.py

backend: ## Run the FastAPI backend (http://localhost:8001)
	cd $(BACKEND_DIR) && ../$(VENV)/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)

frontend: ## Run the Vite dev server (http://localhost:5173)
	cd $(FRONTEND_DIR) && npm run dev

dev: ## Run backend + frontend together (Ctrl-C stops both)
	@echo "Starting backend on :$(BACKEND_PORT) and frontend on :5173 ..."
	@trap 'kill 0' INT TERM EXIT; \
	(cd $(BACKEND_DIR) && ../$(VENV)/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port $(BACKEND_PORT)) & \
	(cd $(FRONTEND_DIR) && npm run dev) & \
	wait

# ── Docker ──────────────────────────────────────────────────────────────────

build: ## Build Docker images
	docker compose build

up: ## Start the full stack in Docker (frontend http://localhost:8080)
	docker compose up -d --build

down: ## Stop the Docker stack
	docker compose down

logs: ## Tail Docker logs
	docker compose logs -f

# ── Housekeeping ─────────────────────────────────────────────────────────────

clean: ## Remove venv, node_modules, db and Python caches
	rm -rf $(VENV) $(FRONTEND_DIR)/node_modules $(BACKEND_DIR)/crm.db
	find $(BACKEND_DIR) -type d -name __pycache__ -exec rm -rf {} +
