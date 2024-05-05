const express = require('express');
const bodyParser = require('body-parser');
const stripe = require('stripe')('sua_chave_secreta_do_stripe');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Rota para página inicial
app.get('/', (req, res) => {
  res.send('Bem-vindo ao Casino Online!');
});

// Rota para criar uma sessão de checkout
app.post('/criar-sessao-checkout', async (req, res) => {
  const { valor, descricao } = req.body;

  const session = await stripe.checkout.sessions.create({
    payment_method_types: ['card'],
    line_items: [
      {
        price_data: {
          currency: 'brl',
          product_data: {
            name: descricao,
          },
          unit_amount: valor * 100, // Valor em centavos
        },
        quantity: 1,
      },
    ],
    mode: 'payment',
    success_url: 'https://seu-site.com/sucesso',
    cancel_url: 'https://seu-site.com/cancelamento',
  });

  res.json({ id: session.id });
});

// Rota para verificar o pagamento
app.post('/verificar-pagamento', async (req, res) => {
  const { sessionId } = req.body;

  const session = await stripe.checkout.sessions.retrieve(sessionId);

  res.json({ pago: session.payment_status === 'paid' });
});

// Rota para o evento de sucesso do pagamento
app.get('/sucesso', (req, res) => {
  res.send('Pagamento realizado com sucesso! Obrigado por sua compra.');
});

// Rota para o evento de cancelamento do pagamento
app.get('/cancelamento', (req, res) => {
  res.send('O pagamento foi cancelado. Por favor, tente novamente.');
});

// Inicia o servidor
app.listen(PORT, () => {
  console.log(`Servidor iniciado na porta ${PORT}`);
});
