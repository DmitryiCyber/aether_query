//! AetherQuery Rust Client
//! 
//! Library and CLI for interacting with AetherQuery servers

pub mod cli;
pub mod output;
pub mod client;

// Re-export main types
pub use cli::{Cli, Command, OutputFormat};
pub use output::OutputFormatter;
pub use client::AetherClient;
