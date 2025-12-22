package core

import (
	"encoding/json"
	"fmt"
	"time"
)

// AetherClient - основной клиент для работы с AetherQuery
type AetherClient struct {
	baseURL    string
	httpClient *HTTPClient
	options    ClientOptions
}

// ClientOptions - опции клиента
type ClientOptions struct {
	APIKey     string
	SQLKey     string
	Timeout    time.Duration
	MaxRetries int
	RetryDelay time.Duration
	Headers    map[string]string
}

// NewClient создает новый экземпляр клиента
func NewClient(baseURL string, options ...ClientOption) *AetherClient {
	opts := ClientOptions{
		Timeout:    30 * time.Second,
		MaxRetries: 3,
		RetryDelay: 1 * time.Second,
		Headers:    make(map[string]string),
	}

	// Применяем переданные опции
	for _, option := range options {
		option(&opts)
	}

	httpClient := NewHTTPClient(HTTPOptions{
		BaseURL:    baseURL,
		Timeout:    opts.Timeout,
		MaxRetries: opts.MaxRetries,
		RetryDelay: opts.RetryDelay,
		Headers:    opts.Headers,
	})

	// Устанавливаем авторизацию
	if opts.APIKey != "" {
		httpClient.SetHeader("X-API-Key", opts.APIKey)
	}
	if opts.SQLKey != "" {
		httpClient.SetHeader("X-SQL-Key", opts.SQLKey)
	}

	return &AetherClient{
		baseURL:    baseURL,
		httpClient: httpClient,
		options:    opts,
	}
}

// ClientOption - функциональная опция для конфигурации клиента
type ClientOption func(*ClientOptions)

func WithAPIKey(apiKey string) ClientOption {
	return func(o *ClientOptions) {
		o.APIKey = apiKey
	}
}

func WithSQLKey(sqlKey string) ClientOption {
	return func(o *ClientOptions) {
		o.SQLKey = sqlKey
	}
}

func WithTimeout(timeout time.Duration) ClientOption {
	return func(o *ClientOptions) {
		o.Timeout = timeout
	}
}

func WithMaxRetries(retries int) ClientOption {
	return func(o *ClientOptions) {
		o.MaxRetries = retries
	}
}

func WithHeader(key, value string) ClientOption {
	return func(o *ClientOptions) {
		if o.Headers == nil {
			o.Headers = make(map[string]string)
		}
		o.Headers[key] = value
	}
}

// ExecuteQuery выполняет одиночный SQL запрос
func (c *AetherClient) ExecuteQuery(query string, params []interface{}, options *QueryOptions) (*QueryResponse, error) {
	request := QueryRequest{
		Query:   query,
		Params:  params,
		Options: options,
	}

	data, err := json.Marshal(request)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %v", err)
	}

	response, err := c.httpClient.Post("/query", data)
	if err != nil {
		return nil, err
	}

	var queryResponse QueryResponse
	if err := json.Unmarshal(response, &queryResponse); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	return &queryResponse, nil
}

// ExecuteBatch выполняет пакет запросов
func (c *AetherClient) ExecuteBatch(queries []QueryRequest, transaction bool) (*BatchResponse, error) {
	request := BatchRequest{
		Queries:     queries,
		Transaction: transaction,
	}

	data, err := json.Marshal(request)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request: %v", err)
	}

	response, err := c.httpClient.Post("/batch", data)
	if err != nil {
		return nil, err
	}

	var batchResponse BatchResponse
	if err := json.Unmarshal(response, &batchResponse); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	return &batchResponse, nil
}

// Health проверяет доступность сервера
func (c *AetherClient) Health() (*HealthResponse, error) {
	response, err := c.httpClient.Get("/health")
	if err != nil {
		return nil, err
	}

	var healthResponse HealthResponse
	if err := json.Unmarshal(response, &healthResponse); err != nil {
		return nil, fmt.Errorf("failed to unmarshal response: %v", err)
	}

	return &healthResponse, nil
}

// SetBaseURL обновляет базовый URL
func (c *AetherClient) SetBaseURL(baseURL string) {
	c.baseURL = baseURL
	c.httpClient.SetBaseURL(baseURL)
}

// SetAuth устанавливает ключи авторизации
func (c *AetherClient) SetAuth(apiKey, sqlKey string) {
	c.options.APIKey = apiKey
	c.options.SQLKey = sqlKey

	if apiKey != "" {
		c.httpClient.SetHeader("X-API-Key", apiKey)
	} else {
		c.httpClient.RemoveHeader("X-API-Key")
	}

	if sqlKey != "" {
		c.httpClient.SetHeader("X-SQL-Key", sqlKey)
	} else {
		c.httpClient.RemoveHeader("X-SQL-Key")
	}
}
