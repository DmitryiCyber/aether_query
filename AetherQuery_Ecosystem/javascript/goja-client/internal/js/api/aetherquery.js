/**
 * AetherQuery JavaScript Client API
 * ES6 модуль для работы с AetherQuery сервером
 */

/**
 * HTTP клиент для работы с AetherQuery API
 */
class AetherHTTPClient {
    constructor(baseURL, options = {}) {
        this.baseURL = baseURL.replace(/\/$/, '');
        this.options = {
            timeout: 30000,
            retries: 3,
            retryDelay: 1000,
            ...options
        };
    }

    async request(method, endpoint, data = null) {
        const url = this.baseURL + endpoint;
        
        try {
            // Используем встроенные binding'и Goja для HTTP запросов
            const response = await http.request({
                method: method,
                url: url,
                headers: {
                    'Content-Type': 'application/json',
                    ...this.options.headers
                },
                body: data ? JSON.stringify(data) : undefined,
                timeout: this.options.timeout
            });

            if (response.status >= 400) {
                throw new Error(`HTTP ${response.status}: ${response.body}`);
            }

            return JSON.parse(response.body);
        } catch (error) {
            throw new Error(`HTTP request failed: ${error.message}`);
        }
    }

    async post(endpoint, data) {
        return await this.request('POST', endpoint, data);
    }

    async get(endpoint) {
        return await this.request('GET', endpoint);
    }
}

/**
 * Основной клиент AetherQuery
 */
export class AetherQueryClient {
    constructor(baseURL, options = {}) {
        this._http = new AetherHTTPClient(baseURL, options);
    }

    /**
     * Выполнить SQL запрос
     */
    async query(sql, params = []) {
        const response = await this._http.post('/query', {
            query: sql,
            params: Array.isArray(params) ? params : [params]
        });

        if (!response.success) {
            throw new AetherQueryError(
                response.error?.message || 'Query failed',
                response.error?.code || 'QUERY_ERROR'
            );
        }

        return new QueryResult(response);
    }

    /**
     * Проверить доступность сервера
     */
    async health() {
        return await this._http.get('/health');
    }

    /**
     * Выполнить запрос и вернуть массив объектов
     */
    async fetchObjects(sql, params = []) {
        const result = await this.query(sql, params);
        return result.toObjects();
    }

    /**
     * Выполнить запрос и вернуть первый объект
     */
    async fetchOne(sql, params = []) {
        const objects = await this.fetchObjects(sql, params);
        return objects[0] || null;
    }

    /**
     * Выполнить запрос и вернуть значение первой колонки первой строки
     */
    async fetchValue(sql, params = []) {
        const result = await this.query(sql, params);
        return result.rows[0]?.[0] || null;
    }
}

/**
 * Результат выполнения запроса
 */
export class QueryResult {
    constructor(response) {
        this.success = response.success;
        this.query = response.query;
        this.executionTime = response.execution_time;
        this.affectedRows = response.affected_rows || 0;
        this.lastInsertId = response.last_insert_id || 0;
        
        this._result = response.result || {};
    }

    get columns() {
        return this._result.columns || [];
    }

    get rows() {
        return this._result.rows || [];
    }

    get rowCount() {
        return this._result.row_count || 0;
    }

    /**
     * Конвертировать результат в массив объектов
     */
    toObjects() {
        return this.rows.map(row => {
            const obj = {};
            this.columns.forEach((column, index) => {
                obj[column] = row[index];
            });
            return obj;
        });
    }

    /**
     * Получить первую строку как объект
     */
    first() {
        const objects = this.toObjects();
        return objects[0] || null;
    }

    /**
     * Проверить есть ли данные
     */
    hasData() {
        return this.rowCount > 0;
    }
}

/**
 * Кастомная ошибка AetherQuery
 */
export class AetherQueryError extends Error {
    constructor(message, code) {
        super(message);
        this.name = 'AetherQueryError';
        this.code = code;
    }
}

/**
 * Фабрика для создания клиентов
 */
export function createClient(baseURL, options = {}) {
    return new AetherQueryClient(baseURL, options);
}

/**
 * Быстрые функции для простых сценариев
 */
export async function query(baseURL, sql, params = []) {
    const client = createClient(baseURL);
    return await client.query(sql, params);
}

export async function fetchObjects(baseURL, sql, params = []) {
    const client = createClient(baseURL);
    return await client.fetchObjects(sql, params);
}

export async function health(baseURL) {
    const client = createClient(baseURL);
    return await client.health();
}

/**
 * Default export - основной API объект
 */
export default {
    // Фабричные методы
    createClient,
    
    // Быстрые методы
    query,
    fetchObjects,
    health,
    
    // Классы
    Client: AetherQueryClient,
    Result: QueryResult,
    Error: AetherQueryError
};