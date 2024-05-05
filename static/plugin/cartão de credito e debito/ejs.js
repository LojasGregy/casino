const express = require('express');
const app = express();
const ejs = require('ejs');

app.set('view engine', 'ejs');

// Rota para o evento de sucesso do pagamento
app.get('/sucesso', (req, res) => {
  res.render('sucesso');
});

// Rota para o evento de cancelamento do pagamento
app.get('/cancelamento', (req, res) => {
  res.render('cancelamento');
});

app.listen(3000, () => {
  console.log('Servidor iniciado na porta 3000');
});
