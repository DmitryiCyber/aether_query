/**
 * HTTP клиент для Goja (биндинги к Go)
 */

class HTTPResponse {
    constructor(data, status, headers) {
        this.data = data;
        this.status = status;
        this.headers = headers || {};
    }

    json() {
        return this.data;
    }

    text() {
        return typeof this.data === 'string' ? this.data : JSON.stringify(this.data);
    }

    ok() {
        return this.status >= 200 && this.status < 300;
    }
}

// Глобальные функции которые будут связаны с Go
globalThis.__aether_http = {
    post: async (url, data, options) => {
        // Эта функция будет реализована в Go
        throw new Error('HTTP post not implemented in Go bindings');
    },
    
    get: async (url, options) => {
        // Эта функция будет реализована в Go  
        throw new Error('HTTP get not implemented in Go bindings');
    }
};

console.log('✅ HTTP client bindings loaded');