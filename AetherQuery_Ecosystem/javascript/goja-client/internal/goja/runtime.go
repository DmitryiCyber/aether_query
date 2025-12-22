package goja

import (
	"fmt"
	"bufio"
	"os"
	"github.com/dop251/goja"
)

type Runtime struct {
	vm *goja.Runtime
}

func NewRuntime() (*Runtime, error) {
	vm := goja.New()
	
	runtime := &Runtime{
		vm: vm,
	}

	// Загружаем модули при создании runtime
	if err := runtime.LoadModules(); err != nil {
		return nil, fmt.Errorf("failed to load modules: %w", err)
	}

	return runtime, nil
}

func (r *Runtime) Close() {
	// Cleanup resources if needed
}

func (r *Runtime) LoadModules() error {
	// Простейшие модули в виде строк
	modules := map[string]string{
		"aetherquery": `
			aetherquery = {
				version: '1.0.0',
				query: function(sql) { 
					return { 
						sql: sql,
						execute: function() {
							return Promise.resolve({ rows: [], columns: [] });
						}
					}; 
				},
				health: function(endpoint) { 
					return { 
						status: 'healthy',
						endpoint: endpoint 
					}; 
				},
				connect: function(config) {
					return {
						config: config,
						query: function(sql) { return aetherquery.query(sql); },
						close: function() { return Promise.resolve(); }
					};
				}
			};
		`,
		"utils": `
			utils = {
				formatDate: function(date) { 
					return date ? new Date(date).toISOString() : new Date().toISOString(); 
				},
				delay: function(ms) {
					return new Promise(function(resolve) { setTimeout(resolve, ms); });
				}
			};
		`,
	}

	for name, source := range modules {
		_, err := r.vm.RunString(source)
		if err != nil {
			return fmt.Errorf("failed to load module %s: %w", name, err)
		}
	}
	
	return nil
}

func (r *Runtime) RunScript(scriptPath string) error {
	code, err := os.ReadFile(scriptPath)
	if err != nil {
		return fmt.Errorf("failed to read script: %v", err)
	}

	_, err = r.vm.RunString(string(code))
	return err
}

func (r *Runtime) RunString(code string) (goja.Value, error) {
	return r.vm.RunString(code)
}

func (r *Runtime) StartREPL() {
	fmt.Println("JavaScript REPL - Type .exit to quit")

	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Print("js> ")
		if !scanner.Scan() {
			break
		}

		input := scanner.Text()
		if input == ".exit" || input == "exit" || input == "quit" {
			break
		}

		if input == "" {
			continue
		}

		val, err := r.vm.RunString(input)
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			continue
		}

		if val != nil && !goja.IsUndefined(val) {
			fmt.Println(val.String())
		}
	}
}

