import redis from 'redis';

const client = redis.createClient();

// Function to create a hash
const createHash = () => {
  client.hset(
    'HolbertonSchools',
    {
      Portland: 50,
      Seattle: 80,
      'New York': 20,
      Bogota: 20,
      Cali: 40,
      Paris: 2,
    },
    redis.print
  );
};

const displayHash = () => {
  client.hgetall('HolbertonSchools', (err, reply) => {
    console.log(reply);
  });
};

createHash();
displayHash();
