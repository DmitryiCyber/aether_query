// Minimal aetherquery module
aetherquery = {
    version: '1.0.0',
    query: function(sql) {
        return { sql: sql };
    },
    health: function() {
        return { status: 'ok' };
    }
};