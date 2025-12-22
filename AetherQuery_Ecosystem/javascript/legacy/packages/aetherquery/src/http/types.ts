export interface HTTPClientOptions {
  baseURL: string;
  timeout?: number;
  maxRetries?: number;
  retryDelay?: number;
  headers?: Record<string, string>;
  apiKey?: string;
  sqlKey?: string;
}

export interface RequestConfig {
  headers?: Record<string, string>;
  timeout?: number;
  retry?: boolean;
}

export interface RetryConfig {
  maxRetries: number;
  retryDelay: number;
  retryCondition: (error: any) => boolean;
}