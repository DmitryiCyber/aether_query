import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { HTTPClientOptions, RequestConfig } from './types';
import { retryWithBackoff } from './retry';
import { AetherQueryError, createErrorFromResponse } from '../errors';

export class HttpClient {
  private client: AxiosInstance;
  private options: HTTPClientOptions;

  constructor(options: HTTPClientOptions) {
    this.options = {
      timeout: 30000,
      maxRetries: 3,
      retryDelay: 1000,
      headers: {},
      ...options
    };

    this.client = axios.create({
      baseURL: this.options.baseURL,
      timeout: this.options.timeout,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': 'AetherQuery-JS-Client/1.0.0',
        ...this.options.headers
      }
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor - добавление авторизации
    this.client.interceptors.request.use(
      (config: { headers: { [x: string]: string; }; }) => {
        // Добавляем API ключ если есть
        if (this.options.apiKey) {
          config.headers['X-API-Key'] = this.options.apiKey;
        }
        
        // Добавляем SQL ключ если есть
        if (this.options.sqlKey) {
          config.headers['X-SQL-Key'] = this.options.sqlKey;
        }

        return config;
      },
      (error: any) => Promise.reject(error)
    );

    // Response interceptor - обработка ошибок
    this.client.interceptors.response.use(
      (response: any) => response,
      (error: any) => {
        const aetherError = createErrorFromResponse(error);
        return Promise.reject(aetherError);
      }
    );
  }

  async get<T>(path: string, config?: RequestConfig): Promise<T> {
    return this.request<T>('GET', path, undefined, config);
  }

  async post<T>(path: string, data?: any, config?: RequestConfig): Promise<T> {
    return this.request<T>('POST', path, data, config);
  }

  async put<T>(path: string, data?: any, config?: RequestConfig): Promise<T> {
    return this.request<T>('PUT', path, data, config);
  }

  async delete<T>(path: string, config?: RequestConfig): Promise<T> {
    return this.request<T>('DELETE', path, undefined, config);
  }

  private async request<T>(
    method: string,
    path: string,
    data?: any,
    config?: RequestConfig
  ): Promise<T> {
    const requestConfig: AxiosRequestConfig = {
      method,
      url: path,
      data: method !== 'GET' ? data : undefined,
      params: method === 'GET' ? data : undefined,
      headers: config?.headers,
      timeout: config?.timeout
    };

    const shouldRetry = config?.retry !== false;

    if (shouldRetry && this.options.maxRetries && this.options.maxRetries > 0) {
      return retryWithBackoff(
        () => this.executeRequest<T>(requestConfig),
        this.options.maxRetries,
        this.options.retryDelay || 1000
      );
    }

    return this.executeRequest<T>(requestConfig);
  }

  private async executeRequest<T>(config: AxiosRequestConfig): Promise<T> {
    try {
      const response: AxiosResponse<T> = await this.client.request<T>(config);
      return response.data;
    } catch (error) {
      // Error is already transformed by interceptor
      throw error;
    }
  }

  // Public methods for configuration updates
  setBaseURL(baseURL: string): void {
    this.options.baseURL = baseURL;
    this.client.defaults.baseURL = baseURL;
  }

  setAuth(apiKey?: string, sqlKey?: string): void {
    this.options.apiKey = apiKey;
    this.options.sqlKey = sqlKey;
  }

  setHeaders(headers: Record<string, string>): void {
    this.options.headers = { ...this.options.headers, ...headers };
    this.client.defaults.headers = {
      ...this.client.defaults.headers,
      ...headers
    } as any;
  }

  getBaseURL(): string {
    return this.options.baseURL;
  }
}