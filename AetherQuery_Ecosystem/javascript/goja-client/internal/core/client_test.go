package core

import (
	"testing"
	"time"
)

func TestNewClient(t *testing.T) {
	client := NewClient("http://localhost:8000/api/v1")
	if client == nil {
		t.Fatal("Expected client to be created")
	}
}

func TestClientWithOptions(t *testing.T) {
	client := NewClient(
		"http://localhost:8000/api/v1",
		WithAPIKey("test-key"),
		WithSQLKey("sql-key"),
		WithTimeout(10*time.Second),
		WithMaxRetries(5),
	)

	if client == nil {
		t.Fatal("Expected client to be created with options")
	}
}

func TestClientSetAuth(t *testing.T) {
	client := NewClient("http://localhost:8000/api/v1")
	client.SetAuth("new-api-key", "new-sql-key")
	// Тестируем что заголовки установились (нужен mock HTTP клиент)
}

func TestErrorMapping(t *testing.T) {
	tests := []struct {
		statusCode int
		expected   string
	}{
		{400, "BAD_REQUEST"},
		{401, "UNAUTHORIZED"},
		{403, "FORBIDDEN"},
		{422, "VALIDATION_ERROR"},
		{500, "SERVER_ERROR"},
		{999, "UNKNOWN_ERROR"},
	}

	for _, test := range tests {
		err := ErrorMapper(test.statusCode, "test message", nil)
		if err.Code != test.expected {
			t.Errorf("For status %d, expected %s, got %s", test.statusCode, test.expected, err.Code)
		}
	}
}

func TestIsConnectionError(t *testing.T) {
	connError := &AetherError{Code: "NETWORK_ERROR"}
	if !IsConnectionError(connError) {
		t.Error("Expected NETWORK_ERROR to be connection error")
	}

	serverError := &AetherError{Code: "SERVER_ERROR", HTTPCode: 500}
	if !IsConnectionError(serverError) {
		t.Error("Expected 500 error to be connection error")
	}

	validationError := &AetherError{Code: "VALIDATION_ERROR", HTTPCode: 422}
	if IsConnectionError(validationError) {
		t.Error("Expected validation error not to be connection error")
	}
}
