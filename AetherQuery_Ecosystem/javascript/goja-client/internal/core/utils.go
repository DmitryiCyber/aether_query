package core

import "fmt"

// ResultToObjects конвертирует QueryResponse в массив объектов
func ResultToObjects(response *QueryResponse) ([]map[string]interface{}, error) {
	if response.Result == nil {
		return []map[string]interface{}{}, nil
	}
	return response.Result.AllToMaps(), nil
}

// FirstRow возвращает первую строку как объект
func FirstRow(response *QueryResponse) (map[string]interface{}, error) {
	if response.Result == nil || len(response.Result.Rows) == 0 {
		return nil, nil
	}
	return response.Result.RowToMap(0), nil
}

// FirstValue возвращает значение первой колонки первой строки
func FirstValue(response *QueryResponse) (interface{}, error) {
	if response.Result == nil || len(response.Result.Rows) == 0 {
		return nil, nil
	}
	if len(response.Result.Rows[0]) == 0 {
		return nil, nil
	}
	return response.Result.Rows[0][0], nil
}

// ValidateResponse проверяет успешность ответа
func ValidateResponse(response *QueryResponse) error {
	if !response.Success {
		if response.Error != nil {
			return fmt.Errorf("[%s] %s", response.Error.Code, response.Error.Message)
		}
		return fmt.Errorf("query execution failed")
	}
	return nil
}

// QuickQuery выполняет запрос и возвращает объекты
func (c *AetherClient) QuickQuery(query string, params []interface{}) ([]map[string]interface{}, error) {
	response, err := c.ExecuteQuery(query, params, nil)
	if err != nil {
		return nil, err
	}

	if err := ValidateResponse(response); err != nil {
		return nil, err
	}

	return ResultToObjects(response)
}

// QuickValue выполняет запрос и возвращает одно значение
func (c *AetherClient) QuickValue(query string, params []interface{}) (interface{}, error) {
	response, err := c.ExecuteQuery(query, params, nil)
	if err != nil {
		return nil, err
	}

	if err := ValidateResponse(response); err != nil {
		return nil, err
	}

	return FirstValue(response)
}
