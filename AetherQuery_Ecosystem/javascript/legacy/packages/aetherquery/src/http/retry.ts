import { AetherQueryError } from '../errors';

export async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  maxRetries: number,
  baseDelay: number
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error as Error;

      // Не повторяем для определенных ошибок
      if (error instanceof AetherQueryError) {
        if ([400, 401, 403, 422].includes(error.statusCode || 0)) {
          throw error;
        }
      }

      // Последняя попытка?
      if (attempt === maxRetries) {
        break;
      }

      // Экспоненциальная backoff задержка
      const delay = baseDelay * Math.pow(2, attempt);
      await sleep(delay);
    }
  }

  throw lastError!;
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}