package goja

import (
	"fmt"

	"github.com/dop251/goja"
)

func (r *Runtime) initConsoleBindings() error {
	consoleObj := r.vm.NewObject()

	// Биндинги для console.log
	consoleObj.Set("log", func(call goja.FunctionCall) goja.Value {
		args := make([]interface{}, len(call.Arguments))
		for i, arg := range call.Arguments {
			args[i] = arg.Export()
		}
		fmt.Println(args...)
		return goja.Undefined()
	})

	consoleObj.Set("error", func(call goja.FunctionCall) goja.Value {
		args := make([]interface{}, len(call.Arguments))
		for i, arg := range call.Arguments {
			args[i] = arg.Export()
		}
		fmt.Print("ERROR: ")
		fmt.Println(args...)
		return goja.Undefined()
	})

	consoleObj.Set("warn", func(call goja.FunctionCall) goja.Value {
		args := make([]interface{}, len(call.Arguments))
		for i, arg := range call.Arguments {
			args[i] = arg.Export()
		}
		fmt.Print("WARN: ")
		fmt.Println(args...)
		return goja.Undefined()
	})

	consoleObj.Set("info", func(call goja.FunctionCall) goja.Value {
		args := make([]interface{}, len(call.Arguments))
		for i, arg := range call.Arguments {
			args[i] = arg.Export()
		}
		fmt.Print("INFO: ")
		fmt.Println(args...)
		return goja.Undefined()
	})

	return r.vm.Set("console", consoleObj)
}
