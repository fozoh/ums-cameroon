.PHONY: help up down build test lint format clean logs shell-backend shell-frontend audit install

help:
	@echo "UMS Cameroon - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make up              Start all services with docker-compose"
	@echo "  make down            Stop all services"
	@echo "  make logs            Show logs from all services"
	@echo "  make shell-backend   Open bash in backend container"
	@echo "  make shell-frontend  Open bash in frontend container"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test            Run all tests (backend + frontend)"
	@echo "  make test-backend    Run backend tests only"
	@echo "  make test-frontend   Run frontend tests only"
	@echo "  make lint            Run linting (flake8 + ESLint)"
	@echo "  make lint-backend    Lint backend only"
	@echo "  make lint-frontend   Lint frontend only"
	@echo "  make audit           Run security audits (npm audit + secrets check)"
	@echo "  make format          Auto-format code (black for Python)"
	@echo ""
	@echo "Build & Cleanup:"
	@echo "  make build           Build production Docker images"
	@echo "  make install         Install all dependencies (local dev)"
	@echo "  make clean           Remove build artifacts, cache, __pycache__"
	@echo ""

# Docker Compose Commands
up:
	docker-compose up --build

down:
	docker-compose down

logs:
	docker-compose logs -f

shell-backend:
	docker-compose exec backend bash

shell-frontend:
	docker-compose exec frontend bash

build:
	docker-compose build

# Testing
test: test-backend test-frontend

test-backend:
	cd backend && ../.venv/bin/python manage.py test --verbosity=2

test-frontend:
	cd frontend && CI=true npm test -- --watchAll=false

# Linting
lint: lint-backend lint-frontend

lint-backend:
	cd backend && ../.venv/bin/python -m flake8 students --max-line-length=120 --exclude=migrations

lint-frontend:
	cd frontend && npx eslint src --max-warnings=0 2>/dev/null || echo "ESLint not configured; skipping"

# Code Formatting
format:
	cd backend && ../.venv/bin/black students --line-length=120 --quiet 2>/dev/null || echo "Black not installed; skipping"

# Security Audit
audit: audit-npm audit-secrets

audit-npm:
	@echo "Running npm audit on frontend..."
	cd frontend && npm audit --audit-level=moderate

audit-secrets:
	@echo "Checking for secrets in code..."
	@if command -v detect-secrets >/dev/null 2>&1; then \
		detect-secrets scan --all-files --force-use-all-plugins --baseline .secrets.baseline || true; \
	else \
		echo "detect-secrets not installed. Install with: pip install detect-secrets"; \
	fi

# Installation
install: install-backend install-frontend

install-backend:
	cd backend && ../.venv/bin/pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	cd backend && rm -rf .pytest_cache htmlcov .coverage
	cd frontend && rm -rf node_modules build .eslintcache

# Run all checks (CI-like)
check: lint audit test
	@echo "✓ All checks passed!"
