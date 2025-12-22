using System;
using System.IO;
using System.Runtime.InteropServices;

public class WasmClient : IDisposable
{
    private IntPtr _wasmModule = IntPtr.Zero;
    private IntPtr _wasmInstance = IntPtr.Zero;
    private bool _initialized = false;

    public void Initialize(string wasmPath)
    {
        if (!File.Exists(wasmPath))
        {
            throw new FileNotFoundException($"WASM file not found: {wasmPath}");
        }

        try
        {
            // Загрузка WASM модуля
            byte[] wasmBytes = File.ReadAllBytes(wasmPath);
            _wasmModule = LoadWasmModule(wasmBytes, wasmBytes.Length);

            if (_wasmModule == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to load WASM module");
            }

            // Инициализация инстанса
            _wasmInstance = CreateWasmInstance(_wasmModule);

            if (_wasmInstance == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create WASM instance");
            }

            _initialized = true;
            Console.WriteLine($"✅ WASM module loaded successfully from: {wasmPath}");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Failed to initialize WASM: {ex.Message}");
            throw;
        }
    }

    public string Health()
    {
        if (!_initialized)
        {
            return "❌ WASM module not initialized";
        }

        try
        {
            // Вызов функции health из WASM модуля
            var result = CallWasmFunction(_wasmInstance, "health", null, 0);
            return result ?? "✅ Health check passed";
        }
        catch (Exception ex)
        {
            return $"❌ Health check failed: {ex.Message}";
        }
    }

    public string Query(string sqlQuery)
    {
        if (!_initialized)
        {
            throw new InvalidOperationException("WASM module not initialized");
        }

        if (string.IsNullOrEmpty(sqlQuery))
        {
            throw new ArgumentException("SQL query cannot be empty");
        }

        try
        {
            // Вызов функции query из WASM модуля
            var result = CallWasmFunction(_wasmInstance, "query", sqlQuery, sqlQuery.Length);
            return result ?? $"Query executed: {sqlQuery}";
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Query failed: {ex.Message}", ex);
        }
    }

    public void Dispose()
    {
        if (_wasmInstance != IntPtr.Zero)
        {
            DestroyWasmInstance(_wasmInstance);
            _wasmInstance = IntPtr.Zero;
        }

        if (_wasmModule != IntPtr.Zero)
        {
            UnloadWasmModule(_wasmModule);
            _wasmModule = IntPtr.Zero;
        }

        _initialized = false;
        Console.WriteLine("WasmClient disposed");
    }

    // Нативные методы для работы с WASM (заглушки - нужно реализовать с помощью библиотеки)
    [DllImport("wasmtime", EntryPoint = "wasm_module_load")]
    private static extern IntPtr LoadWasmModule(byte[] bytes, int length);

    [DllImport("wasmtime", EntryPoint = "wasm_instance_create")]
    private static extern IntPtr CreateWasmInstance(IntPtr module);

    [DllImport("wasmtime", EntryPoint = "wasm_function_call")]
    private static extern string CallWasmFunction(IntPtr instance, string functionName, string? input, int inputLength);

    [DllImport("wasmtime", EntryPoint = "wasm_instance_destroy")]
    private static extern void DestroyWasmInstance(IntPtr instance);

    [DllImport("wasmtime", EntryPoint = "wasm_module_unload")]
    private static extern void UnloadWasmModule(IntPtr module);
}