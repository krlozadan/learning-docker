const express = require('express');
const redis = require('redis');

// Redis setup
const client = redis.createClient({ host: 'redis-server', port: 6379 });
client.on('error', err => console.log('Redis client error', err));
client.set('visits', 1);

// Express setup
const app = express();
const PORT = 8080;

app.get('/', (req, res) => {
    client.get('visits', (err, visits) => {
        res.send(`Number of visits: ${visits}`);
        client.incr('visits');
    })
});

app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
});