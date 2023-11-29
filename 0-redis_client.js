import redis from 'redis';

const client = redis.createClient();

client.on('connect', () => {
  console.log('Redis Client connected to the server');
});

client.on('error', (err) => {
  console.log(`Redis Client not connected to the server ${err}`);
});

client.quit();
