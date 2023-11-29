import redis from 'redis';
import { promisify } from 'util';

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

const displaySchoolValue = async (schoolName) => {
  const reply = await getAsync(schoolName);
  console.log(reply);
};

displaySchoolValue('Holberton');
