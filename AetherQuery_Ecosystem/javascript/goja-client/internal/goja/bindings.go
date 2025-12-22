package goja

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/aetherquery/goja-client/internal/core"

	"github.com/dop251/goja"
)

func (r *Runtime) initGoBindings() error {
	// HTTP биндинги
	if err := r.initHTTPBindings(); err != nil {
		return err
	}

	// Console биндинги
	if err := r.initConsoleBindings(); err != nil {
		return err
	}

	// FS биндинги (опционально)
	if err := r.initFSBindings(); err != nil {
		return err
	}

	return nil
}

func (r *Runtime) initHTTPBindings() error {
	// Биндинг для __aether_http.post
	err := r.vm.Set("__aether_http", map[string]interface{}{
		"post": func(call goja.FunctionCall) goja.Value {
			url := call.Argument(0).String()
			data := call.Argument(1).Export()
			options := call.Argument(2).Export()

			// Создаем временный клиент для этого запроса
			httpOpts := core.HTTPOptions{
				Timeout:    30 * time.Second,
				MaxRetries: 3,
				RetryDelay: 1 * time.Second,
			}

			if opts, ok := options.(map[string]interface{}); ok {
				if timeout, ok := opts["timeout"].(float64); ok {
					httpOpts.Timeout = time.Duration(timeout) * time.Millisecond
				}
				if retries, ok := opts["retries"].(float64); ok {
					httpOpts.MaxRetries = int(retries)
				}
				if retryDelay, ok := opts["retryDelay"].(float64); ok {
					httpOpts.RetryDelay = time.Duration(retryDelay) * time.Millisecond
				}
			}

			client := core.NewHTTPClient(httpOpts)

			// Конвертируем данные в JSON
			jsonData, err := json.Marshal(data)
			if err != nil {
				return r.createErrorResult(fmt.Sprintf("Failed to marshal data: %v", err))
			}

			// Выполняем запрос
			response, err := client.Post(url, jsonData)
			if err != nil {
				return r.createErrorResult(err.Error())
			}

			// Парсим JSON ответ
			var result map[string]interface{}
			if err := json.Unmarshal(response, &result); err != nil {
				return r.createErrorResult(fmt.Sprintf("Failed to parse response: %v", err))
			}

			return r.vm.ToValue(result)
		},

		"get": func(call goja.FunctionCall) goja.Value {
			url := call.Argument(0).String()
			options := call.Argument(1).Export()

			httpOpts := core.HTTPOptions{
				Timeout:    30 * time.Second,
				MaxRetries: 3,
				RetryDelay: 1 * time.Second,
			}

			if opts, ok := options.(map[string]interface{}); ok {
				if timeout, ok := opts["timeout"].(float64); ok {
					httpOpts.Timeout = time.Duration(timeout) * time.Millisecond
				}
			}

			client := core.NewHTTPClient(httpOpts)

			response, err := client.Get(url)
			if err != nil {
				return r.createErrorResult(err.Error())
			}

			var result map[string]interface{}
			if err := json.Unmarshal(response, &result); err != nil {
				return r.createErrorResult(fmt.Sprintf("Failed to parse response: %v", err))
			}

			return r.vm.ToValue(result)
		},
	})

	return err
}

func (r *Runtime) createErrorResult(message string) goja.Value {
	return r.vm.ToValue(map[string]interface{}{
		"error": message,
	})
}
