generate:
	uvx openapi-python-client generate \
		--path openapi-1.8.3.json \
		--config openapi-python-client-config.yml \
		--meta uv \
		--overwrite

install:
	uv pip install -e .

fmt:
	uvx ruff format .
	uvx ruff check --fix .

test:
	uvx --with tox-uv tox
