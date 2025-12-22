package main

import (
	"fmt"
	"log"
	"os"
	"path/filepath"

	"github.com/aetherquery/goja-client/internal/goja"
)

func main() {
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}

	command := os.Args[1]

	switch command {
	case "run":
		if len(os.Args) < 3 {
			fmt.Println("Usage: aetherquery run <script.js>")
			os.Exit(1)
		}
		runScript(os.Args[2])
	case "repl":
		runREPL()
	case "eval":
		if len(os.Args) < 3 {
			fmt.Println("Usage: aetherquery eval '<code>'")
			os.Exit(1)
		}
		evalCode(os.Args[2])
	case "version":
		printVersion()
	default:
		// Если первый аргумент - файл .js, выполняем его
		if filepath.Ext(command) == ".js" {
			runScript(command)
		} else {
			printUsage()
		}
	}
}

func runScript(scriptPath string) {
	runtime, err := goja.NewRuntime()
	if err != nil {
		log.Fatalf("Failed to initialize runtime: %v", err)
	}
	defer runtime.Close()

	// Загружаем стандартные модули
	if err := runtime.LoadModules(); err != nil {
		log.Fatalf("Failed to load modules: %v", err)
	}

	// Выполняем скрипт
	if err := runtime.RunScript(scriptPath); err != nil {
		log.Fatalf("Script execution failed: %v", err)
	}
}

func runREPL() {
	fmt.Println("AetherQuery JavaScript REPL")
	fmt.Println("Type 'exit' or 'quit' to exit")
	fmt.Println()

	runtime, err := goja.NewRuntime()
	if err != nil {
		log.Fatalf("Failed to initialize runtime: %v", err)
	}
	defer runtime.Close()

	if err := runtime.LoadModules(); err != nil {
		log.Fatalf("Failed to load modules: %v", err)
	}

	runtime.StartREPL()
}

func evalCode(code string) {
	runtime, err := goja.NewRuntime()
	if err != nil {
		log.Fatalf("Failed to initialize runtime: %v", err)
	}
	defer runtime.Close()

	if err := runtime.LoadModules(); err != nil {
		log.Fatalf("Failed to load modules: %v", err)
	}

	if _, err := runtime.RunString(code); err != nil {
		log.Fatalf("Evaluation failed: %v", err)
	}
}

func printUsage() {
	fmt.Println(`AetherQuery Goja Client - JavaScript runtime for AetherQuery

Usage:
  aetherquery run <script.js>    Run a JavaScript file
  aetherquery repl               Start REPL environment  
  aetherquery eval '<code>'      Evaluate JavaScript code
  aetherquery version            Show version
  aetherquery <file.js>          Run JavaScript file (shortcut)

Examples:
  aetherquery run examples/basic-query.js
  aetherquery repl
  aetherquery eval "aetherquery.health('http://localhost:8000')"`)
}

func printVersion() {
	fmt.Println("AetherQuery Goja Client v1.0.0")
}
