package goja

import (
	"os"

	"github.com/dop251/goja"
)

func (r *Runtime) initFSBindings() error {
	fsObj := r.vm.NewObject()

	fsObj.Set("readFile", func(call goja.FunctionCall) goja.Value {
		filename := call.Argument(0).String()

		content, err := os.ReadFile(filename)
		if err != nil {
			return r.vm.ToValue(map[string]interface{}{
				"error": err.Error(),
			})
		}

		return r.vm.ToValue(string(content))
	})

	fsObj.Set("writeFile", func(call goja.FunctionCall) goja.Value {
		filename := call.Argument(0).String()
		content := call.Argument(1).String()

		err := os.WriteFile(filename, []byte(content), 0644)
		if err != nil {
			return r.vm.ToValue(map[string]interface{}{
				"error": err.Error(),
			})
		}

		return r.vm.ToValue(true)
	})

	fsObj.Set("exists", func(call goja.FunctionCall) goja.Value {
		filename := call.Argument(0).String()

		_, err := os.Stat(filename)
		exists := err == nil

		return r.vm.ToValue(exists)
	})

	return r.vm.Set("fs", fsObj)
}
