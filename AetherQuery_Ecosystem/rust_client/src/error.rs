// src/error.rs
use thiserror::Error;

#[derive(Debug, Error)]
pub enum ClientError {
    #[error("HTTP error: {0}")]
    HttpError(String),
    
    #[error("WASM error: {0}")]
    WasmError(String),
    
    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),
    
    #[error("Network error: {0}")]
    NetworkError(String),
    
    #[error("Server error: {0}")]
    ServerError(String),
    
    #[error("Not implemented")]
    NotImplemented,
}

pub type Result<T> = std::result::Result<T, ClientError>;