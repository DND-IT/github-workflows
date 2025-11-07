NAME:=github-workflows
REQUIREMENTS:=requirements.txt

.PHONY: gen_docs_install gen_docs

gen_docs_install:
	@echo "Installing gen docs cli"
	cd ./docs/.scripts/gen_docs && npm install && npm link

gen_docs_run: gen_docs_install
	@echo "Generating docs"
	gen-docs

docker-build: $(REQUIREMENTS)
	docker build -t $(NAME) .

docker-run: docker-build
	docker run -v $$(pwd):/app -p 8000:8000 --rm --name $(NAME) -t $(NAME)

.venv/.requirements-installed: $(REQUIREMENTS)
	@echo "📦 Creating Python virtual environment..."
	@python -m venv .venv
	@echo "🔄 Installing dependencies..."
	@. .venv/bin/activate && pip install -r $(REQUIREMENTS)
	@touch .venv/.requirements-installed
	@echo "✅ Virtual environment ready!"

serve-docs: .venv/.requirements-installed
	@echo "🚀 Starting MkDocs server..."
	@. .venv/bin/activate && mkdocs serve
