# AetherQuery Goja Client Makefile

# Variables
BINARY_NAME=aetherquery
GO_VERSION=1.25.4-1
BUILD_DIR=dist
EXAMPLES_DIR=examples
TEST_DIR=.

# Default target
all: build test

# Build the binary
build:
	@echo "Building $(BINARY_NAME)..."
	@go build -o $(BINARY_NAME) main.go
	@echo "Build complete: ./$(BINARY_NAME)"

# Build for multiple platforms
build-all: build-linux build-darwin build-windows

build-linux:
	@echo "Building for Linux..."
	@GOOS=linux GOARCH=amd64 go build -o $(BUILD_DIR)/linux/$(BINARY_NAME) main.go

build-darwin:
	@echo "Building for macOS..."
	@GOOS=darwin GOARCH=amd64 go build -o $(BUILD_DIR)/darwin/$(BINARY_NAME) main.go

build-windows:
	@echo "Building for Windows..."
	@GOOS=windows GOARCH=amd64 go build -o $(BUILD_DIR)/windows/$(BINARY_NAME).exe main.go

# Install dependencies
deps:
	@echo "Installing dependencies..."
	@go mod tidy
	@go mod download

# Run tests
test:
	@echo "Running tests..."
	@go test -v ./internal/core/...
	@go test -v ./internal/goja/...

test-core:
	@echo "Testing core package..."
	@go test -v ./internal/core/...

test-goja:
	@echo "Testing goja package..."
	@go test -v ./internal/goja/...

test-verbose:
	@echo "Running verbose tests..."
	@go test -v -cover ./...

test-coverage:
	@echo "Running tests with coverage..."
	@go test -coverprofile=coverage.out ./...
	@go tool cover -html=coverage.out -o coverage.html
	@echo "Coverage report generated: coverage.html"

# Run examples
run-examples:
	@echo "Running examples..."
	@for example in $(shell find $(EXAMPLES_DIR) -name "*.js"); do \
		echo "=== Running $$example ==="; \
		./$(BINARY_NAME) run $$example; \
		echo ""; \
	done

run-basic:
	@echo "Running basic example..."
	@./$(BINARY_NAME) run examples/basic-query.js

run-batch:
	@echo "Running batch example..."
	@./$(BINARY_NAME) run examples/batch-operations.js

run-cli:
	@echo "Running CLI example..."
	@./$(BINARY_NAME) run examples/cli-tool.js

# Development
dev:
	@echo "Starting development mode..."
	@go run main.go

repl:
	@echo "Starting REPL..."
	@go run main.go repl

clean:
	@echo "Cleaning up..."
	@rm -f $(BINARY_NAME)
	@rm -rf $(BUILD_DIR)
	@rm -f coverage.out coverage.html
	@go clean

# Code quality
lint:
	@echo "Running linter..."
	@go fmt ./...
	@go vet ./...

check-imports:
	@echo "Checking imports..."
	@goimports -l .

# Integration tests (requires AetherQuery server)
test-integration:
	@echo "Running integration tests..."
	@echo "Note: This requires a running AetherQuery server"
	@go test -v -tags=integration ./internal/core/...

# Benchmarking
bench:
	@echo "Running benchmarks..."
	@go test -bench=. -benchmem ./internal/core/...

# Docker
docker-build:
	@echo "Building Docker image..."
	@docker build -t aetherquery-goja .

docker-run:
	@echo "Running in Docker..."
	@docker run -it aetherquery-goja

# Release preparation
release: clean build-all
	@echo "Creating release packages..."
	@tar -czf $(BUILD_DIR)/aetherquery-linux-amd64.tar.gz -C $(BUILD_DIR)/linux $(BINARY_NAME)
	@tar -czf $(BUILD_DIR)/aetherquery-darwin-amd64.tar.gz -C $(BUILD_DIR)/darwin $(BINARY_NAME)
	@zip -j $(BUILD_DIR)/aetherquery-windows-amd64.zip $(BUILD_DIR)/windows/$(BINARY_NAME).exe
	@echo "Release packages created in $(BUILD_DIR)/"

# Help
help:
	@echo "Available targets:"
	@echo "  build        - Build the binary"
	@echo "  build-all    - Build for all platforms"
	@echo "  test         - Run all tests"
	@echo "  test-core    - Test core package only"
	@echo "  test-goja    - Test goja package only"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  run-examples - Run all examples"
	@echo "  run-basic    - Run basic example"
	@echo "  repl         - Start REPL"
	@echo "  lint         - Format and vet code"
	@echo "  clean        - Clean build artifacts"
	@echo "  docker-build - Build Docker image"
	@echo "  release      - Prepare release packages"
	@echo "  help         - Show this help"

.PHONY: all build build-all deps test test-core test-goja test-coverage run-examples run-basic run-batch run-cli dev repl clean lint check-imports test-integration bench docker-build docker-run release help