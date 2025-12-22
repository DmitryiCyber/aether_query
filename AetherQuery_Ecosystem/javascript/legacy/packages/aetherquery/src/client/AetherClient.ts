import { HttpClient } from '../http/HttpClient';
import { 
  QueryRequest, 
  QueryResponse, 
  BatchRequest, 
  BatchResponse, 
  HealthResponse 
} from '../models';
import { ClientOptions, ExecuteQueryOptions } from './types';

export class AetherClient {
  private httpClient: HttpClient;

  constructor(options: ClientOptions) {
    this.httpClient = new HttpClient(options);
  }

  /**
   * Execute a single SQL query
   */
  async executeQuery(
    query: string, 
    options: ExecuteQueryOptions = {}
  ): Promise<QueryResponse> {
    const request: QueryRequest = {
      query,
      params: options.params,
      options: options.options
    };

    return await this.httpClient.post<QueryResponse>('/query', request);
  }

  /**
   * Execute multiple SQL queries in a batch
   */
  async executeBatch(
    queries: string[], 
    transaction: boolean = true
  ): Promise<BatchResponse> {
    const request: BatchRequest = {
      queries: queries.map(query => ({ query })),
      transaction
    };

    return await this.httpClient.post<BatchResponse>('/batch', request);
  }

  /**
   * Check server health
   */
  async health(): Promise<HealthResponse> {
    return await this.httpClient.get<HealthResponse>('/health');
  }

  /**
   * Set authentication tokens
   */
  setAuth(apiKey?: string, sqlKey?: string): void {
    this.httpClient.setAuth(apiKey, sqlKey);
  }

  /**
   * Update base URL
   */
  setBaseURL(baseURL: string): void {
    this.httpClient.setBaseURL(baseURL);
  }
}