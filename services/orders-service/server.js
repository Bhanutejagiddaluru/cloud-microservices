import express from 'express';
const app = express();
const PORT = process.env.PORT || 7000;

app.get('/health', (_, res) => res.json({status:'ok', service:'orders'}));
app.get('/orders', (_, res) => {
  res.json([
    { id: 1, total: 29.99, status: 'DELIVERED' },
    { id: 2, total: 58.40, status: 'PROCESSING' }
  ]);
});

app.listen(PORT, () => console.log(`orders-service listening on ${PORT}`));
