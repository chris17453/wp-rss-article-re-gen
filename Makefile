# Makefile for Singularity Sentinel

.PHONY: help run clean

# Variables
PYTHON=python
MAIN_SCRIPT=singularity_sentinel.cli
PIPENV=pipenv
REQUIREMENTS=requirements.txt

help:
	@echo "Usage:"
	@echo "  make setup       Set up the Python virtual environment and install dependencies."
	@echo "  make run         Run the AI news system."
	@echo "  make clean       Clean up the environment."

setup:
	@echo "Setting up the virtual environment..."
	@if [ ! -d $(VENV_DIR) ]; then $(PYTHON) -m venv $(VENV_DIR); fi
	@$(VENV_DIR)/bin/pip install --upgrade pip
	@$(VENV_DIR)/bin/pip install -r $(REQUIREMENTS)
	@echo "Setup complete."

run:
	@echo "Running the AI news system..."
	@if command -v pipenv > /dev/null; then \
	$(PIPENV) run $(PYTHON) -m $(MAIN_SCRIPT); \
else \
	$(PYTHON) -m $(MAIN_SCRIPT); \
fi
