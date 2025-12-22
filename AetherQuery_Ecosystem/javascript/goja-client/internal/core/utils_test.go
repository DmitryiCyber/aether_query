package core

import (
	"testing"
)

func TestResultToObjects(t *testing.T) {
	response := &QueryResponse{
		Success: true,
		Result: &QueryResult{
			Columns: []string{"id", "name"},
			Rows: [][]interface{}{
				{1, "John"},
				{2, "Jane"},
			},
			RowCount: 2,
		},
	}

	objects, err := ResultToObjects(response)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if len(objects) != 2 {
		t.Errorf("Expected 2 objects, got %d", len(objects))
	}

	if objects[0]["name"] != "John" {
		t.Errorf("Expected first object name to be 'John', got %v", objects[0]["name"])
	}
}

func TestFirstRow(t *testing.T) {
	response := &QueryResponse{
		Success: true,
		Result: &QueryResult{
			Columns: []string{"id", "name"},
			Rows: [][]interface{}{
				{1, "John"},
			},
			RowCount: 1,
		},
	}

	first, err := FirstRow(response)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if first["name"] != "John" {
		t.Errorf("Expected first row name to be 'John', got %v", first["name"])
	}
}

func TestFirstValue(t *testing.T) {
	response := &QueryResponse{
		Success: true,
		Result: &QueryResult{
			Columns: []string{"count"},
			Rows: [][]interface{}{
				{42},
			},
			RowCount: 1,
		},
	}

	value, err := FirstValue(response)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}

	if value != 42 {
		t.Errorf("Expected first value to be 42, got %v", value)
	}
}
