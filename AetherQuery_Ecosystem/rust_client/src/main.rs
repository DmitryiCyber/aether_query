use rust_client::{Cli, OutputFormatter, AetherClient};
use clap::Parser;
use std::path::PathBuf;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let cli = Cli::parse();
    
    // Create output formatter
    let formatter = OutputFormatter::new(cli.format.clone(), cli.verbose);
    
    // Create client
    let client = AetherClient::new(&cli.server);
    
    // Используем публичное поле verbose напрямую
    if cli.verbose {
        formatter.success(&format!("Connecting to server: {}", cli.server));
    }
    
    // Execute command
    match cli.command {
        rust_client::Command::Query { query, output } => {
            execute_query(&client, &query, &formatter, output).await?;
        }
        rust_client::Command::Batch { file, stop_on_error } => {
            execute_batch(&client, &file, &formatter, stop_on_error).await?;
        }
        rust_client::Command::Shell => {
            interactive_shell(&client, &formatter).await?;
        }
        rust_client::Command::Status => {
            check_status(&client, &formatter).await?;
        }
        rust_client::Command::Tables { pattern } => {
            list_tables(&client, &formatter, pattern.as_deref()).await?;
        }
        rust_client::Command::Describe { table } => {
            describe_table(&client, &formatter, &table).await?;
        }
    }
    
    Ok(())
}

/// Execute a single query
async fn execute_query(
    client: &AetherClient,
    query: &str,
    formatter: &OutputFormatter,
    output_file: Option<PathBuf>,
) -> Result<(), Box<dyn std::error::Error>> {
    // Используем formatter.verbose напрямую
    if formatter.verbose {
        formatter.success(&format!("Executing query: {}", query));
    }
    
    let result = client.execute_query(query).await?;
    
    if let Some(path) = &output_file {  // Берем ссылку здесь
        std::fs::write(path, &result)?;
        formatter.success(&format!("Results saved to: {:?}", path));  // Используем ту же ссылку
    } else {
        formatter.display_results(&result)?;
    }
    
    Ok(())
}

/// Execute queries from a file
async fn execute_batch(
    client: &AetherClient,
    file: &PathBuf,
    formatter: &OutputFormatter,
    stop_on_error: bool,
) -> Result<(), Box<dyn std::error::Error>> {
    let content = std::fs::read_to_string(file)?;
    
    // Split by semicolons or newlines
    let queries: Vec<&str> = content
        .split(';')
        .filter(|q| !q.trim().is_empty())
        .collect();
    
    // Используем formatter.verbose напрямую
    if formatter.verbose {
        formatter.success(&format!("Found {} queries to execute", queries.len()));
    }
    
    for (i, query) in queries.iter().enumerate() {
        let query = query.trim();
        if query.is_empty() {
            continue;
        }
        
        if formatter.verbose {
            println!("\nQuery {}/{}:", i + 1, queries.len());
            println!("{}", query);
            println!("{}", "-".repeat(50));
        }
        
        match client.execute_query(query).await {
            Ok(result) => {
                formatter.display_results(&result)?;
            }
            Err(e) => {
                formatter.error(&format!("Failed to execute query: {}", e));
                if stop_on_error {
                    return Err(e.into());
                }
            }
        }
    }
    
    if formatter.verbose {
        formatter.success("Batch execution completed");
    }
    
    Ok(())
}

/// Interactive SQL shell
async fn interactive_shell(
    client: &AetherClient,
    formatter: &OutputFormatter,
) -> Result<(), Box<dyn std::error::Error>> {
    println!("🦀 AetherQuery Interactive Shell");
    println!("Type \\? for help, \\q to quit\n");
    
    let mut rl = rustyline::DefaultEditor::new()?;
    let mut current_format = formatter.format.clone();
    
    loop {
        let readline = rl.readline("aether> ");
        match readline {
            Ok(line) => {
                let line = line.trim();
                
                // Handle special commands
                match line {
                    "\\?" | "\\h" => formatter.display_help(),
                    "\\q" | "\\quit" => break,
                    "\\t" => {
                        list_tables(client, formatter, None).await.ok();
                        continue;
                    }
                    "\\s" => {
                        check_status(client, formatter).await.ok();
                        continue;
                    }
                    _ if line.starts_with("\\d ") => {
                        let table = line[3..].trim();
                        describe_table(client, formatter, table).await.ok();
                        continue;
                    }
                    _ if line.starts_with("\\f ") => {
                        let new_format = line[3..].trim();
                        match new_format.to_lowercase().as_str() {
                            "table" => current_format = rust_client::OutputFormat::Table,
                            "json" => current_format = rust_client::OutputFormat::Json,
                            "csv" => current_format = rust_client::OutputFormat::Csv,
                            "markdown" => current_format = rust_client::OutputFormat::Markdown,
                            "raw" => current_format = rust_client::OutputFormat::Raw,
                            _ => println!("Unknown format. Available: table, json, csv, markdown, raw"),
                        }
                        println!("Output format changed to: {:?}", current_format);
                        continue;
                    }
                    _ => {}
                }
                
                // Skip empty lines
                if line.is_empty() {
                    continue;
                }
                
                // Execute SQL query
                rl.add_history_entry(line)?;
                match client.execute_query(line).await {
                    Ok(result) => {
                        let temp_formatter = OutputFormatter::new(current_format.clone(), false);
                        temp_formatter.display_results(&result)?;
                    }
                    Err(e) => {
                        formatter.error(&format!("Error: {}", e));
                    }
                }
            }
            Err(_) => {
                break;
            }
        }
    }
    
    println!("Goodbye!");
    Ok(())
}

/// Check server status
async fn check_status(
    client: &AetherClient,
    formatter: &OutputFormatter,
) -> Result<(), Box<dyn std::error::Error>> {
    if formatter.verbose {
        formatter.info("Checking server health...");
    }
    
    let status = client.check_health().await?;
    formatter.display_results(&status)?;
    
    Ok(())
}

/// List tables
async fn list_tables(
    client: &AetherClient,
    formatter: &OutputFormatter,
    pattern: Option<&str>,
) -> Result<(), Box<dyn std::error::Error>> {
    let query = if let Some(pattern) = pattern {
        format!("SHOW TABLES LIKE '{}'", pattern)
    } else {
        "SHOW TABLES".to_string()
    };
    
    if formatter.verbose {
        formatter.info(&format!("Listing tables with pattern: {:?}", pattern));
    }
    
    let result = client.execute_query(&query).await?;
    formatter.display_results(&result)?;
    
    Ok(())
}

/// Describe table structure
async fn describe_table(
    client: &AetherClient,
    formatter: &OutputFormatter,
    table: &str,
) -> Result<(), Box<dyn std::error::Error>> {
    let query = format!("DESCRIBE {}", table);
    
    if formatter.verbose {
        formatter.info(&format!("Describing table: {}", table));
    }
    
    let result = client.execute_query(&query).await?;
    formatter.display_results(&result)?;
    
    Ok(())
}