package core

// QueryRequest - запрос на выполнение SQL
type QueryRequest struct {
	Query   string        `json:"query"`
	Params  []interface{} `json:"params,omitempty"`
	Options *QueryOptions `json:"options,omitempty"`
}

// QueryOptions - дополнительные опции запроса
type QueryOptions struct {
	Timeout  *float64 `json:"timeout,omitempty"`
	ReadOnly *bool    `json:"read_only,omitempty"`
	MaxRows  *int     `json:"max_rows,omitempty"`
}

// BatchRequest - запрос на выполнение пакета SQL запросов
type BatchRequest struct {
	Queries     []QueryRequest `json:"queries"`
	Transaction bool           `json:"transaction"`
}

// QueryResult - результат выполнения запроса
type QueryResult struct {
	Columns       []string        `json:"columns"`
	Rows          [][]interface{} `json:"rows"`
	RowCount      int             `json:"row_count"`
	ExecutionTime *float64        `json:"execution_time,omitempty"`
}

// QueryResponse - ответ на выполнение запроса
type QueryResponse struct {
	Success       bool         `json:"success"`
	Query         string       `json:"query"`
	Result        *QueryResult `json:"result,omitempty"`
	ExecutionTime *float64     `json:"execution_time,omitempty"`
	AffectedRows  *int         `json:"affected_rows,omitempty"`
	LastInsertID  *int64       `json:"last_insert_id,omitempty"`
	Error         *ErrorDetail `json:"error,omitempty"`
}

// BatchResponse - ответ на выполнение пакета запросов
type BatchResponse struct {
	Success            bool            `json:"success"`
	Results            []QueryResponse `json:"results"`
	TotalExecutionTime *float64        `json:"total_execution_time,omitempty"`
}

// HealthResponse - ответ проверки здоровья
type HealthResponse struct {
	Status    string  `json:"status"`
	Timestamp string  `json:"timestamp"`
	Version   *string `json:"version,omitempty"`
	Database  *string `json:"database,omitempty"`
}

// ErrorDetail - детали ошибки
type ErrorDetail struct {
	Code    string      `json:"code"`
	Message string      `json:"message"`
	Details interface{} `json:"details,omitempty"`
}

// RowToMap конвертирует строку результата в map
func (qr *QueryResult) RowToMap(rowIndex int) map[string]interface{} {
	if rowIndex < 0 || rowIndex >= len(qr.Rows) {
		return nil
	}

	result := make(map[string]interface{})
	for colIndex, column := range qr.Columns {
		result[column] = qr.Rows[rowIndex][colIndex]
	}
	return result
}

// AllToMaps конвертирует все строки в массив map
func (qr *QueryResult) AllToMaps() []map[string]interface{} {
	var results []map[string]interface{}
	for i := 0; i < len(qr.Rows); i++ {
		results = append(results, qr.RowToMap(i))
	}
	return results
}

// GetValue возвращает значение по индексу строки и колонки
func (qr *QueryResult) GetValue(rowIndex, colIndex int) interface{} {
	if rowIndex < 0 || rowIndex >= len(qr.Rows) {
		return nil
	}
	if colIndex < 0 || colIndex >= len(qr.Rows[rowIndex]) {
		return nil
	}
	return qr.Rows[rowIndex][colIndex]
}

// GetColumn возвращает все значения колонки
func (qr *QueryResult) GetColumn(colIndex int) []interface{} {
	var column []interface{}
	for _, row := range qr.Rows {
		if colIndex < len(row) {
			column = append(column, row[colIndex])
		}
	}
	return column
}

// GetColumnByName возвращает все значения колонки по имени
func (qr *QueryResult) GetColumnByName(columnName string) []interface{} {
	for i, col := range qr.Columns {
		if col == columnName {
			return qr.GetColumn(i)
		}
	}
	return nil
}
