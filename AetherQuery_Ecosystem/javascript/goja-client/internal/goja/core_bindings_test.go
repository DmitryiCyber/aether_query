package goja

import (
	"testing"
)

// TestRuntimeCreation проверяет что runtime создается без ошибок
func TestRuntimeCreation(t *testing.T) {
	runtime, err := NewRuntime()
	if err != nil {
		t.Fatalf("Failed to create runtime: %v", err)
	}
	defer runtime.Close()

	if runtime == nil {
		t.Error("Runtime should not be nil")
	}
}

// TestBasicJavaScript проверяет базовое выполнение JavaScript
func TestBasicJavaScript(t *testing.T) {
	runtime, err := NewRuntime()
	if err != nil {
		t.Fatalf("Failed to create runtime: %v", err)
	}
	defer runtime.Close()

	// Тестируем простые выражения
	tests := []struct {
		name     string
		code     string
		expected int64
	}{
		{"Addition", "2 + 2", 4},
		{"Multiplication", "3 * 5", 15},
		{"Subtraction", "10 - 3", 7},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result, err := runtime.RunString(tt.code)
			if err != nil {
				t.Errorf("Failed to execute %s: %v", tt.code, err)
				return
			}

			value := result.ToInteger()
			if value != tt.expected {
				t.Errorf("For %s expected %d, got %d", tt.code, tt.expected, value)
			}
		})
	}
}

// TestStringOperations проверяет строковые операции
func TestStringOperations(t *testing.T) {
	runtime, err := NewRuntime()
	if err != nil {
		t.Fatalf("Failed to create runtime: %v", err)
	}
	defer runtime.Close()

	result, err := runtime.RunString("'Hello' + ' ' + 'World'")
	if err != nil {
		t.Errorf("Failed to execute string expression: %v", err)
		return
	}

	if result.String() != "Hello World" {
		t.Errorf("Expected 'Hello World', got '%s'", result.String())
	}
}

// TestObjectOperations проверяет работу с объектами
func TestObjectOperations(t *testing.T) {
	runtime, err := NewRuntime()
	if err != nil {
		t.Fatalf("Failed to create runtime: %v", err)
	}
	defer runtime.Close()

	// Создаем объект в JavaScript
	_, err = runtime.RunString("var testObj = { name: 'test', value: 42 }")
	if err != nil {
		t.Errorf("Failed to create object: %v", err)
		return
	}

	// Читаем свойства объекта
	result, err := runtime.RunString("testObj.value")
	if err != nil {
		t.Errorf("Failed to read object property: %v", err)
		return
	}

	if result.ToInteger() != 42 {
		t.Errorf("Expected 42, got %d", result.ToInteger())
	}
}
