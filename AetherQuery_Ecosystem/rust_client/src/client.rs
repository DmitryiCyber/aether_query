use reqwest::Client;

/// AetherQuery HTTP Client
pub struct AetherClient {
    base_url: String,
    client: Client,
}

impl AetherClient {
    /// Create a new AetherQuery client
    pub fn new(base_url: &str) -> Self {
        Self {
            base_url: base_url.trim_end_matches('/').to_string(),
            client: Client::new(),
        }
    }
    
    /// Check server health
    pub async fn check_health(&self) -> Result<String, Box<dyn std::error::Error>> {
        let url = format!("{}/health", self.base_url);
        let response = self.client.get(&url).send().await?;
        
        if response.status().is_success() {
            Ok(response.text().await?)
        } else {
            Err(format!("Server returned status: {}", response.status()).into())
        }
    }
    
    /// Execute a SQL query
    pub async fn execute_query(&self, query: &str) -> Result<String, Box<dyn std::error::Error>> {
        let url = format!("{}/query", self.base_url);
        let response = self.client
            .get(&url)
            .query(&[("q", query)])
            .send()
            .await?;
        
        if response.status().is_success() {
            Ok(response.text().await?)
        } else {
            Err(format!("Query failed with status: {}", response.status()).into())
        }
    }
}