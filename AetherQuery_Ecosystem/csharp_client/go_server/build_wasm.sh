#!/bin/bash
cd /second_disk/My_Projects/aether_query/AetherQuery_Ecosystem/go_server

echo "🔧 Собираем WASM..."
GOOS=js GOARCH=wasm go build -o aether.wasm wasm.go

echo "📦 Копируем в C# проект..."
cp aether.wasm ../csharp_client/wasm_modules/

echo "✅ Готово! Размер: $(du -h aether.wasm | cut -f1)"