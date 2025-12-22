use crate::cli::OutputFormat;
use serde_json::Value;
use std::io;

/// Formats and outputs query results
pub struct OutputFormatter {
    pub format: OutputFormat,
    pub verbose: bool,
}

impl OutputFormatter {
    pub fn new(format: OutputFormat, verbose: bool) -> Self {
        Self { format, verbose }
    }
    
    /// Display a success message
    pub fn success(&self, message: &str) {
        if self.verbose {
            println!("✅ {}", message);
        }
    }
    
    /// Display an error message
    pub fn error(&self, message: &str) {
        eprintln!("❌ {}", message);
    }
    
    /// Display an info message (always shows)
    pub fn info(&self, message: &str) {
        println!("ℹ️ {}", message);
    }
    
    /// Display query results
    pub fn display_results(&self, results: &str) -> io::Result<()> {
        match self.format {
            OutputFormat::Table => self.display_table(results),
            OutputFormat::Json => self.display_json(results),
            OutputFormat::Csv => self.display_csv(results),
            OutputFormat::Markdown => self.display_markdown(results),
            OutputFormat::Raw => self.display_raw(results),
        }
    }
    
    /// Parse and display as table
    fn display_table(&self, results: &str) -> io::Result<()> {
        // Try to parse as JSON first
        if let Ok(json) = serde_json::from_str::<Value>(results) {
            self.print_json_as_table(&json)?;
        } else {
            // Fallback to raw output
            println!("{}", results);
        }
        Ok(())
    }
    
    /// Display as JSON
    fn display_json(&self, results: &str) -> io::Result<()> {
        // Pretty print if it's valid JSON
        if let Ok(json) = serde_json::from_str::<Value>(results) {
            println!("{}", serde_json::to_string_pretty(&json)?);
        } else {
            println!("{}", results);
        }
        Ok(())
    }
    
    /// Display as CSV
    fn display_csv(&self, results: &str) -> io::Result<()> {
        // Simple CSV output - in real implementation, parse properly
        if let Ok(json) = serde_json::from_str::<Value>(results) {
            self.print_json_as_csv(&json)?;
        } else {
            println!("Result\n\"{}\"", results.replace("\"", "\"\""));
        }
        Ok(())
    }
    
    /// Display as Markdown table
    fn display_markdown(&self, results: &str) -> io::Result<()> {
        if let Ok(json) = serde_json::from_str::<Value>(results) {
            self.print_json_as_markdown(&json)?;
        } else {
            println!("```\n{}\n```", results);
        }
        Ok(())
    }
    
    /// Display raw results
    fn display_raw(&self, results: &str) -> io::Result<()> {
        println!("{}", results);
        Ok(())
    }
    
    /// Helper to print JSON as table
    fn print_json_as_table(&self, json: &Value) -> io::Result<()> {
        // Simplified implementation
        match json {
            Value::Object(obj) => {
                println!("┌──────────────────────────────────────┐");
                for (key, value) in obj {
                    println!("│ {:30} : {:20} │", key, value);
                }
                println!("└──────────────────────────────────────┘");
            }
            Value::Array(arr) => {
                println!("┌──────────────────────────────────────┐");
                for (i, value) in arr.iter().enumerate() {
                    println!("│ [{:3}] : {:30} │", i, value);
                }
                println!("└──────────────────────────────────────┘");
            }
            _ => {
                println!("{:#}", json);
            }
        }
        Ok(())
    }
    
    /// Helper to print JSON as CSV
    fn print_json_as_csv(&self, json: &Value) -> io::Result<()> {
        match json {
            Value::Object(obj) => {
                // Print headers
                let headers: Vec<String> = obj.keys().map(|k| k.to_string()).collect();
                println!("{}", headers.join(","));
                
                // Print values
                let values: Vec<String> = obj.values().map(|v| v.to_string()).collect();
                println!("{}", values.join(","));
            }
            _ => {
                println!("Result\n\"{}\"", json);
            }
        }
        Ok(())
    }
    
    /// Helper to print JSON as markdown table
    fn print_json_as_markdown(&self, json: &Value) -> io::Result<()> {
        match json {
            Value::Object(obj) => {
                // Convert keys to strings and join
                let headers: Vec<String> = obj.keys().map(|k| k.to_string()).collect();
                println!("| {} |", headers.join(" | "));
                
                // Create separator row
                let separator = vec!["---"; obj.len()];
                println!("|{}|", separator.join("|"));
                
                // Convert values to strings and join
                let values: Vec<String> = obj.values().map(|v| v.to_string()).collect();
                println!("| {} |", values.join(" | "));
            }
            _ => {
                println!("```\n{}\n```", json);
            }
        }
        Ok(())
    }
    
    /// Display help for available commands in interactive mode
    pub fn display_help(&self) {
        println!("Available commands:");
        println!("  \\? or \\h      - Show this help");
        println!("  \\q or \\quit   - Quit");
        println!("  \\t            - Show tables");
        println!("  \\d <table>    - Describe table");
        println!("  \\s            - Show status");
        println!("  \\f <format>   - Change output format (table, json, csv, markdown, raw)");
        println!("  SQL query     - Execute SQL statement");
    }
}