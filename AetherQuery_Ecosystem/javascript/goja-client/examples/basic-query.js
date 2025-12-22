// Простой пример использования AetherQuery API

async function main() {
    console.log('🚀 AetherQuery Basic Example\n');
    
    // Создаем клиент
    const client = aetherquery.createClient('http://localhost:8000/api/v1');
    
    try {
        // Проверяем здоровье сервера
        console.log('📡 Checking server health...');
        const health = await client.health();
        console.log(`   Status: ${health.status}`);
        console.log(`   Version: ${health.version}`);
        console.log(`   Database: ${health.database}\n`);
        
        // Выполняем простой запрос
        console.log('🔍 Executing simple query...');
        const result1 = await client.query('SELECT 1 + 1 as sum, NOW() as time');
        console.log(`   Execution time: ${result1.executionTime}s`);
        console.log(`   Data:`, result1.rows, '\n');
        
        // Получаем данные как объекты
        console.log('📊 Fetching as objects...');
        const objects = await client.fetchObjects(`
            SELECT 
                'John' as name, 
                25 as age, 
                'developer' as role
            UNION ALL
            SELECT 
                'Jane' as name, 
                30 as age, 
                'designer' as role
        `);
        
        console.log('   Objects:');
        objects.forEach(obj => {
            console.log(`     - ${obj.name}, ${obj.age} years, ${obj.role}`);
        });
        console.log();
        
        // Демонстрация удобных методов
        console.log('🎯 Using convenience methods...');
        
        const singleValue = await client.fetchValue('SELECT COUNT(*) FROM users');
        console.log(`   User count: ${singleValue}`);
        
        const singleObject = await client.fetchOne('SELECT * FROM users LIMIT 1');
        console.log(`   First user:`, singleObject);
        
    } catch (error) {
        console.error('❌ Error:', error.toString());
        if (error.response) {
            console.error('   Response:', error.response);
        }
    }
}

// Запускаем пример
main().catch(console.error);