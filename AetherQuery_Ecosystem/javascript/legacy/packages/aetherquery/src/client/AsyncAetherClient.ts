import { AetherClient } from './AetherClient';
import { ClientOptions } from './types';

/**
 * Async/Await optimized client with additional convenience methods
 */
export class AsyncAetherClient extends AetherClient {
  constructor(options: ClientOptions) {
    super(options);
  }

  /**
   * Execute query and automatically extract rows
   */
  async queryRows<T = any>(
    query: string, 
    params?: any[]
  ): Promise<T[]> {
    const response = await this.executeQuery(query, { params });
    
    if (!response.success) {
      throw new Error(`Query failed: ${response.error?.message}`);
    }

    if (!response.result) {
      return [];
    }

    // Convert rows to objects using column names
    return response.result.rows.map((row: { [x: string]: any; }) => {
      const obj: any = {};
      response.result!.columns.forEach((column: string | number, index: string | number) => {
        obj[column] = row[index];
      });
      return obj as T;
    });
  }

  /**
   * Execute query and get first row
   */
  async queryFirst<T = any>(
    query: string, 
    params?: any[]
  ): Promise<T | null> {
    const rows = await this.queryRows<T>(query, params);
    return rows[0] || null;
  }

  /**
   * Execute query and get single value
   */
  async queryValue<T = any>(
    query: string, 
    params?: any[]
  ): Promise<T | null> {
    const row = await this.queryFirst<T>(query, params);
    if (!row) return null;
    
    const values = Object.values(row);
    return values[0] as T;
  }
}