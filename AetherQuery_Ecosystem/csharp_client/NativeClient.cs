using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public class NativeClient : IDisposable
{
    private readonly HttpClient _httpClient;
    private readonly string _baseUrl;

    public NativeClient(string baseUrl = "http://localhost:8080")
    {
        _baseUrl = baseUrl;
        _httpClient = new HttpClient
        {
            Timeout = TimeSpan.FromSeconds(30)
        };
    }

    public async Task Initialize()
    {
        try
        {
            Console.WriteLine($"🔗 Connecting to {_baseUrl}...");
            var response = await _httpClient.GetAsync($"{_baseUrl}/health");
            response.EnsureSuccessStatusCode();

            var health = await response.Content.ReadAsStringAsync();
            Console.WriteLine($"✅ Connected! Health: {health}");
        }
        catch (Exception ex)
        {
            throw new InvalidOperationException($"Failed to connect to server: {ex.Message}", ex);
        }
    }

    public async Task<string> Health()
    {
        try
        {
            var response = await _httpClient.GetAsync($"{_baseUrl}/health");
            response.EnsureSuccessStatusCode();

            var json = await response.Content.ReadAsStringAsync();
            return $"✅ Server health: {json}";
        }
        catch (Exception ex)
        {
            return $"❌ Health check failed: {ex.Message}";
        }
    }

    public async Task<string> Query(string sqlQuery)
    {
        try
        {
            // Кодируем SQL запрос для URL
            string encodedQuery = Uri.EscapeDataString(sqlQuery);
            string url = $"{_baseUrl}/query?q={encodedQuery}";

            Console.WriteLine($"🌐 Sending GET request to: {_baseUrl}/query?q=...");

            // Отправляем GET запрос
            var response = await _httpClient.GetAsync(url);

            // Проверяем статус
            if (!response.IsSuccessStatusCode)
            {
                var errorContent = await response.Content.ReadAsStringAsync();
                return $"❌ HTTP Error {(int)response.StatusCode}: {errorContent}";
            }

            // Читаем и парсим JSON ответ
            var jsonResponse = await response.Content.ReadAsStringAsync();

            try
            {
                // Пробуем распарсить JSON для красивого вывода
                using var doc = JsonDocument.Parse(jsonResponse);
                var result = doc.RootElement.GetProperty("result").GetString();
                var rows = doc.RootElement.TryGetProperty("rows", out var rowsProp)
                    ? rowsProp.GetInt32().ToString()
                    : "N/A";

                return $"✅ Result: {result}\n   Rows: {rows}";
            }
            catch
            {
                // Если не JSON, возвращаем как есть
                return $"✅ Response: {jsonResponse}";
            }
        }
        catch (Exception ex)
        {
            return $"❌ Query failed: {ex.Message}";
        }
    }

    public void Dispose()
    {
        _httpClient?.Dispose();
        Console.WriteLine("🔌 NativeClient disposed");
    }
}