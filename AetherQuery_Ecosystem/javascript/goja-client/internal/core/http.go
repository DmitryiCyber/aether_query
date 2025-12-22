package core

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

// HTTPOptions - опции HTTP клиента
type HTTPOptions struct {
	BaseURL    string
	Timeout    time.Duration
	MaxRetries int
	RetryDelay time.Duration
	Headers    map[string]string
}

// HTTPClient - HTTP клиент с повторными попытками
type HTTPClient struct {
	client  *http.Client
	options HTTPOptions
	headers map[string]string
}

// NewHTTPClient создает новый HTTP клиент
func NewHTTPClient(options HTTPOptions) *HTTPClient {
	client := &http.Client{
		Timeout: options.Timeout,
	}

	return &HTTPClient{
		client:  client,
		options: options,
		headers: make(map[string]string),
	}
}

// Post выполняет POST запрос
func (h *HTTPClient) Post(endpoint string, data []byte) ([]byte, error) {
	return h.request("POST", endpoint, data, h.options.MaxRetries)
}

// Get выполняет GET запрос
func (h *HTTPClient) Get(endpoint string) ([]byte, error) {
	return h.request("GET", endpoint, nil, h.options.MaxRetries)
}

// request выполняет HTTP запрос с повторными попытками
func (h *HTTPClient) request(method, endpoint string, data []byte, retries int) ([]byte, error) {
	url := h.options.BaseURL + endpoint

	var body io.Reader
	if data != nil {
		body = bytes.NewReader(data)
	}

	req, err := http.NewRequest(method, url, body)
	if err != nil {
		return nil, &AetherError{
			Code:    "REQUEST_ERROR",
			Message: fmt.Sprintf("Failed to create request: %v", err),
		}
	}

	// Устанавливаем заголовки
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("User-Agent", "AetherQuery-Go-Client/1.0.0")

	for key, value := range h.headers {
		req.Header.Set(key, value)
	}
	for key, value := range h.options.Headers {
		req.Header.Set(key, value)
	}

	// Выполняем запрос
	resp, err := h.client.Do(req)
	if err != nil {
		if retries > 0 {
			time.Sleep(h.options.RetryDelay)
			return h.request(method, endpoint, data, retries-1)
		}
		return nil, &AetherError{
			Code:    "NETWORK_ERROR",
			Message: fmt.Sprintf("Network error: %v", err),
		}
	}
	defer resp.Body.Close()

	// Читаем ответ
	responseBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, &AetherError{
			Code:    "READ_ERROR",
			Message: fmt.Sprintf("Failed to read response: %v", err),
		}
	}

	// Проверяем статус код
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		// Пытаемся распарсить ошибку из ответа
		var errorResp struct {
			Error *ErrorDetail `json:"error"`
		}
		if json.Unmarshal(responseBody, &errorResp) == nil && errorResp.Error != nil {
			return nil, &AetherError{
				Code:     errorResp.Error.Code,
				Message:  errorResp.Error.Message,
				Details:  errorResp.Error.Details,
				HTTPCode: resp.StatusCode,
			}
		}

		// Общая HTTP ошибка
		if retries > 0 && shouldRetry(resp.StatusCode) {
			time.Sleep(h.options.RetryDelay)
			return h.request(method, endpoint, data, retries-1)
		}

		return nil, &AetherError{
			Code:     "HTTP_ERROR",
			Message:  fmt.Sprintf("HTTP %d: %s", resp.StatusCode, string(responseBody)),
			HTTPCode: resp.StatusCode,
		}
	}

	return responseBody, nil
}

// shouldRetry определяет нужно ли повторять запрос для данного статус кода
func shouldRetry(statusCode int) bool {
	return statusCode == http.StatusRequestTimeout ||
		statusCode == http.StatusTooManyRequests ||
		statusCode >= http.StatusInternalServerError
}

// SetHeader устанавливает заголовок
func (h *HTTPClient) SetHeader(key, value string) {
	h.headers[key] = value
}

// RemoveHeader удаляет заголовок
func (h *HTTPClient) RemoveHeader(key string) {
	delete(h.headers, key)
}

// SetBaseURL обновляет базовый URL
func (h *HTTPClient) SetBaseURL(baseURL string) {
	h.options.BaseURL = baseURL
}
