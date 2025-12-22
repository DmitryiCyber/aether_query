using System;
using System.IO;
using System.Threading.Tasks;

class Program
{
    static async Task Main(string[] args)
    {
        Console.WriteLine("Aether Query C# Client");
        Console.WriteLine("======================");

        if (args.Length == 0)
        {
            Console.WriteLine("Usage:");
            Console.WriteLine("  dotnet run -- native    - Connect to Go HTTP server");
            Console.WriteLine("  dotnet run -- wasm      - Use embedded WASM module");
            Console.WriteLine("  dotnet run -- test      - Test both modes");
            return;
        }

        string mode = args[0];

        if (mode == "native")
        {
            await RunNativeMode();
        }
        else if (mode == "wasm")
        {
            await RunWasmMode();
        }
        else if (mode == "test")
        {
            await TestBothModes();
        }
        else
        {
            Console.WriteLine($"Unknown mode: {mode}");
        }
    }

    static async Task RunNativeMode()
    {
        Console.WriteLine("🌐 Native mode - connecting to Go HTTP server...");

        using var client = new NativeClient("http://localhost:8080");

        try
        {
            await client.Initialize();

            Console.WriteLine("\n1. Health check:");
            var health = await client.Health();
            Console.WriteLine(health);

            Console.WriteLine("\n2. Sample queries:");

            var queries = new[]
            {
                "SELECT * FROM users",
                "SHOW TABLES",
                "SELECT COUNT(*) FROM logs"
            };

            foreach (var query in queries)
            {
                Console.WriteLine($"\nQuery: {query}");
                try
                {
                    var result = await client.Query(query);
                    Console.WriteLine($"Result: {result}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error in native mode: {ex.Message}");
        }
    }

    static async Task RunWasmMode()
    {
        Console.WriteLine("⚡ WASM mode - using Go WASM module...");

        var wasmPath = Path.Combine("wasm_modules", "aether_query_simple.wasm");

        if (!File.Exists(wasmPath))
        {
            Console.WriteLine($"❌ WASM file not found: {wasmPath}");
            Console.WriteLine("Please build the WASM module first:");
            Console.WriteLine("  cd ../go_server && ./build_wasm.sh");
            Console.WriteLine("  or copy from: wasm_browser/aether_query_simple.wasm");
            return;
        }

        Console.WriteLine($"📄 Using WASM file: {Path.GetFullPath(wasmPath)}");
        Console.WriteLine($"📏 File size: {new FileInfo(wasmPath).Length / 1024} KB");

        // Используем WasmClientStub (временная заглушка)
        using var client = new WasmClientStub();

        try
        {
            client.Initialize(wasmPath);

            Console.WriteLine("\n1. Health check:");
            var health = client.Health();
            Console.WriteLine(health);

            Console.WriteLine("\n2. Sample queries:");

            var queries = new[]
            {
                "SELECT * FROM users",
                "SHOW TABLES",
                "SELECT COUNT(*) FROM logs",
                "SELECT name, email FROM users WHERE active = true"
            };

            foreach (var query in queries)
            {
                Console.WriteLine($"\nQuery: {query}");
                try
                {
                    var result = client.Query(query);
                    Console.WriteLine($"Result: {result}");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error: {ex.Message}");
                }
            }

            Console.WriteLine($"\n✅ WASM mode completed successfully!");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"❌ Error in WASM mode: {ex.Message}");
            Console.WriteLine($"Stack: {ex.StackTrace}");
        }

        await Task.CompletedTask;
    }

    static async Task TestBothModes()
    {
        Console.WriteLine("🧪 Testing both modes...");

        Console.WriteLine("\n=== Testing WASM mode ===");
        await RunWasmMode();

        Console.WriteLine("\n=== Testing Native mode ===");
        await RunNativeMode();

        Console.WriteLine("\n✅ Testing completed!");
    }
}

// Временная заглушка (удали когда WasmClient будет готов)
public class WasmClientStub : IDisposable
{
    public void Initialize(string wasmPath)
    {
        Console.WriteLine($"⚙️ Initializing WASM from: {wasmPath}");
        Console.WriteLine("⚠️  Using stub implementation - real WASM not connected");
    }

    public string Health()
    {
        return "✅ WASM module is healthy (stub implementation)";
    }

    public string Query(string query)
    {
        return $"📊 Query executed successfully: '{query}'\n   Result: [Sample data from stub]\n   Rows affected: 42\n   Time: 0.001s (stub)";
    }

    public void Dispose()
    {
        Console.WriteLine("🔄 WasmClientStub disposed");
    }
}