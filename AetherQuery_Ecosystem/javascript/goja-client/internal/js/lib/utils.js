/**
 * Вспомогательные функции
 */

export function formatDate(date = new Date()) {
    return date.toISOString();
}

export function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

export function isObject(value) {
    return value !== null && typeof value === 'object' && !Array.isArray(value);
}

export default {
    formatDate,
    delay,
    isObject
};