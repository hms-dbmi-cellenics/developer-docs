#!make
#----------------------------------------
# Settings
#----------------------------------------
.DEFAULT_GOAL := help
#--------------------------------------------------
# Targets
#--------------------------------------------------
install: clean ## Creates venv, and adds biomage as system command
	@echo "Creating virtual env and installing dependencies..."
	@python3 -m venv venv
	@venv/bin/pip3 install --upgrade pip
	@venv/bin/pip3 install -r requirements.txt
	@echo "    [✓]\n"
fmt: ## Formats python files
	@echo "==> Formatting files..."
	@black $(PYTHON_FILES)
	@echo ""
check: ## Checks code for linting/construct errors
	@echo "==> Checking if files are well formatted..."
	@flake8 $(PYTHON_FILES)
	@echo "    [✓]\n"
build: ## Build the diagrams 
	@echo "==> Building diagrams..."
	@venv/bin/python3 *.py
	@echo "    [✓]\n"
clean: ## Cleans up temporary files
	@echo "==> Cleaning up..."
	@find . -name "*.pyc" -exec rm -f {} \;
	@rm -r venv
	@echo "    [✓]"
	@echo ""

.PHONY: install build clean help
help: ## Shows available targets
	@fgrep -h "## " $(MAKEFILE_LIST) | fgrep -v fgrep | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-13s\033[0m %s\n", $$1, $$2}'
