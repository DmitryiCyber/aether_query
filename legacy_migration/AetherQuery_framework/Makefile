.PHONY: clean test install

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -type f -delete
	find . -name "*.pyo" -type f -delete
	find . -name "*.pyd" -type f -delete
	find . -name ".coverage" -type f -delete
	find . -name ".pytest_cache" -type d -exec rm -rf {} +
	echo "✅ Кэш очищен!"

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

dev: clean install test