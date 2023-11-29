import express from 'express';
import redis from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const listProducts = [
  { itemId: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { itemId: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { itemId: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { itemId: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

app.get('/list_products', (req, res) => {
  const products = listProducts.map((product) => ({
    itemId: product.itemId,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
  }));
  res.json(products);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = listProducts.find((p) => p.itemId === itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentQuantity = await getCurrentReservedStockById(itemId);
  res.json({
    itemId: product.itemId,
    itemName: product.name,
    price: product.price,
    initialAvailableQuantity: product.stock,
    currentQuantity,
  });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = listProducts.find((p) => p.itemId === itemId);

  if (!product) {
    return res.json({ status: 'Product not found' });
  }

  const currentQuantity = await getCurrentReservedStockById(itemId);

  if (currentQuantity <= 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }

  await reserveStockById(itemId, 1);

  res.json({ status: 'Reservation confirmed', itemId });
});

const getItemById = (id) => listProducts.find((item) => item.itemId === id);

const reserveStockById = async (itemId, stock) => {
  await setAsync(`item_${itemId}`, stock);
};

const getCurrentReservedStockById = async (itemId) => {
  const result = await getAsync(`item_${itemId}`);
  return result ? parseInt(result, 10) : 0;
};

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
