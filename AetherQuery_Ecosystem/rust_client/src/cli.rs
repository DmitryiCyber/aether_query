use clap::{Parser, Subcommand, ValueEnum};
use std::path::PathBuf;

/// AetherQuery CLI Client
#[derive(Parser, Debug)]
#[command(
    name = "aether-cli",
    author,
    version,
    about = "CLI client for AetherQuery database server",
    long_about = "A powerful command-line interface for querying AetherQuery database servers with support for multiple output formats and interactive mode."
)]
pub struct Cli {
    /// Server URL (e.g., http://localhost:8080)
    #[arg(short, long, env = "AETHER_SERVER", default_value = "http://localhost:8080")]
    pub server: String,
    
    /// Output format
    #[arg(short, long, value_enum, default_value = "table")]
    pub format: OutputFormat,
    
    /// Enable verbose output
    #[arg(short, long, default_value_t = false)]
    pub verbose: bool,
    
    /// Subcommand to execute
    #[command(subcommand)]
    pub command: Command,
}

/// Available output formats
#[derive(Debug, Clone, ValueEnum)]
pub enum OutputFormat {
    /// Human-readable table format
    Table,
    /// JSON format
    Json,
    /// CSV format
    Csv,
    /// Markdown table format
    Markdown,
    /// Raw SQL results
    Raw,
}

/// CLI commands
#[derive(Subcommand, Debug)]
pub enum Command {
    /// Execute a single SQL query
    Query {
        /// SQL query to execute
        query: String,
        
        /// Save output to file
        #[arg(short, long)]
        output: Option<PathBuf>,
    },
    
    /// Execute multiple queries from a file
    Batch {
        /// File containing SQL queries (one per line or separated by ;)
        file: PathBuf,
        
        /// Stop on first error
        #[arg(short = 'e', long, default_value_t = false)]
        stop_on_error: bool,
    },
    
    /// Interactive SQL shell
    Shell,
    
    /// Show server information and health
    Status,
    
    /// List available tables
    Tables {
        /// Filter tables by pattern (e.g., user*)
        pattern: Option<String>,
    },
    
    /// Describe table structure
    Describe {
        /// Table name
        table: String,
    },
}