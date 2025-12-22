export interface ClientOptions {
  baseURL: string;
  apiKey?: string;
  sqlKey?: string;
  timeout?: number;
  maxRetries?: number;
  retryDelay?: number;
  headers?: Record<string, string>;
}

export interface QueryOptions {
  timeout?: number;
  readOnly?: boolean;
  maxRows?: number;
}

export interface ExecuteQueryOptions {
  params?: any[];
  options?: QueryOptions;
}