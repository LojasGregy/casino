const express = require('express');
const bodyParser = require('body-parser');
const PagSeguro = require('pagseguro-nodejs');

const app = express();
const PORT = process.env.PORT || 3000;

// Configure o PagSeguro com suas credenciais
const pagseguro = new PagSeguro({
  email: 'seu_email_pagseguro',
  token: 'seu_token_pagseguro',
  mode: 'sandbox', // 'sandbox' para ambiente de teste, 'production' para ambiente de produção
});

// Middleware para analisar corpos de solicitação
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Rota para criar um pagamento
app.post('/pagamentos', (req, res) => {
  const { valor, descricao } = req.body;

  // Crie uma sessão de pagamento no PagSeguro
  pagseguro.createPaymentRequest({
    currency: 'BRL',
    itemId1: '1',
    itemDescription1: descricao,
    itemAmount1: valor,
  }).then((payment) => {
    // Obtenha a URL de pagamento
    const paymentUrl = payment.paymentLink;

    // Retorne a URL de pagamento para o cliente
    res.json({ sucesso: true, url: paymentUrl });
  }).catch((error) => {
    console.error('Erro ao processar pagamento:', error);
    res.status(500).json({ erro: 'Erro ao processar pagamento' });
  });
});

// Inicia o servidor
app.listen(PORT, () => {
  console.log(`Servidor iniciado na porta ${PORT}`);
});
