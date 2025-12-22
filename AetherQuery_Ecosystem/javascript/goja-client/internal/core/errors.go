package core

import "fmt"

// AetherError - базовая ошибка AetherQuery
type AetherError struct {
	Code     string      `json:"code"`
	Message  string      `json:"message"`
	Details  interface{} `json:"details,omitempty"`
	HTTPCode int         `json:"http_code,omitempty"`
}

// Error реализует интерфейс error
func (e *AetherError) Error() string {
	if e.HTTPCode != 0 {
		return fmt.Sprintf("[%s] HTTP %d: %s", e.Code, e.HTTPCode, e.Message)
	}
	return fmt.Sprintf("[%s] %s", e.Code, e.Message)
}

// Predefined errors
var (
	ErrConnectionFailed = &AetherError{
		Code:    "CONNECTION_FAILED",
		Message: "Failed to connect to AetherQuery server",
	}

	ErrInvalidResponse = &AetherError{
		Code:    "INVALID_RESPONSE",
		Message: "Invalid response from server",
	}

	ErrQueryExecution = &AetherError{
		Code:    "QUERY_EXECUTION_FAILED",
		Message: "Query execution failed",
	}

	ErrAuthentication = &AetherError{
		Code:    "AUTHENTICATION_FAILED",
		Message: "Authentication failed",
	}

	ErrValidation = &AetherError{
		Code:    "VALIDATION_ERROR",
		Message: "Request validation failed",
	}

	ErrTimeout = &AetherError{
		Code:    "TIMEOUT",
		Message: "Request timeout",
	}
)

// ErrorMapper маппит HTTP коды в AetherError
func ErrorMapper(statusCode int, message string, details interface{}) *AetherError {
	switch statusCode {
	case 400:
		return &AetherError{
			Code:     "BAD_REQUEST",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	case 401:
		return &AetherError{
			Code:     "UNAUTHORIZED",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	case 403:
		return &AetherError{
			Code:     "FORBIDDEN",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	case 404:
		return &AetherError{
			Code:     "NOT_FOUND",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	case 422:
		return &AetherError{
			Code:     "VALIDATION_ERROR",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	case 429:
		return &AetherError{
			Code:     "RATE_LIMITED",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	case 500:
		return &AetherError{
			Code:     "SERVER_ERROR",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	case 502, 503, 504:
		return &AetherError{
			Code:     "SERVICE_UNAVAILABLE",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	default:
		return &AetherError{
			Code:     "UNKNOWN_ERROR",
			Message:  message,
			Details:  details,
			HTTPCode: statusCode,
		}
	}
}

// IsConnectionError проверяет является ли ошибка ошибкой соединения
func IsConnectionError(err error) bool {
	if aetherErr, ok := err.(*AetherError); ok {
		return aetherErr.Code == "NETWORK_ERROR" ||
			aetherErr.Code == "CONNECTION_FAILED" ||
			aetherErr.HTTPCode >= 500
	}
	return false
}

// IsAuthenticationError проверяет является ли ошибка ошибкой аутентификации
func IsAuthenticationError(err error) bool {
	if aetherErr, ok := err.(*AetherError); ok {
		return aetherErr.Code == "UNAUTHORIZED" ||
			aetherErr.Code == "FORBIDDEN" ||
			aetherErr.Code == "AUTHENTICATION_FAILED" ||
			aetherErr.HTTPCode == 401 ||
			aetherErr.HTTPCode == 403
	}
	return false
}

// IsValidationError проверяет является ли ошибка ошибкой валидации
func IsValidationError(err error) bool {
	if aetherErr, ok := err.(*AetherError); ok {
		return aetherErr.Code == "VALIDATION_ERROR" ||
			aetherErr.Code == "BAD_REQUEST" ||
			aetherErr.HTTPCode == 400 ||
			aetherErr.HTTPCode == 422
	}
	return false
}

// WrapError оборачивает ошибку в AetherError
func WrapError(err error, code, message string) *AetherError {
	return &AetherError{
		Code:    code,
		Message: fmt.Sprintf("%s: %v", message, err),
	}
}
