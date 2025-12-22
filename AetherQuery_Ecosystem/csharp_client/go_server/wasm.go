//go:build js && wasm
// +build js,wasm

package main

import (
    "syscall/js"
)

func main() {
    // Экспортируем функции в JavaScript
    js.Global().Set("aetherQuery", js.FuncOf(func(this js.Value, args []js.Value) any {
        if len(args) == 0 {
            return "❌ Нет запроса"
        }
        return ProcessQuery(args[0].String())
    }))

    js.Global().Set("aetherHealth", js.FuncOf(func(this js.Value, args []js.Value) any {
        return HealthCheck()
    }))

    // Вечный цикл, чтобы WASM не завершался
    select {}
}