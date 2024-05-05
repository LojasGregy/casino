const express = require('express');
const bodyParser = require('body-parser');
const paypal = require('@paypal/checkout-server-sdk');

const app = express();
const PORT = process.env.PORT || 3000;

// Configure o SDK do PayPal com suas credenciais
const environment = process.env.NODE_ENV === 'production'
  ? new paypal.core.LiveEnvironment('CLIENT_ID_LIVE', 'CLIENT_SECRET_LIVE')
  : new paypal.core.SandboxEnvironment('CLIENT_ID_SANDBOX', 'CLIENT_SECRET_SANDBOX');

const client = new paypal.core.PayPalHttpClient(environment);

// Middleware para analisar corpos de solicitação
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Rota para criar um pagamento
app.post('/pagamentos', async (req, res) => {
  try {
    const { valor, descricao } = req.body;

    // Crie uma ordem de pagamento usando a API do PayPal
    const request = new paypal.orders.OrdersCreateRequest();
    request.prefer("return=representation");
    request.requestBody({
      intent: 'CAPTURE',
      purchase_units: [{
        amount: {
          currency_code: 'BRL',
          value: valor.toFixed(2)
        },
        description: descricao
      }]
    });

    const response = await client.execute(request);

    // Retorna a URL de aprovação do pagamento para o cliente
    res.json({ sucesso: true, url: response.result.links[1].href });
  } catch (error) {
    console.error('Erro ao processar pagamento:', error.message);
    res.status(500).json({ erro: 'Erro ao processar pagamento' });
  }
});

// Inicia o servidor
app.listen(PORT, () => {
  console.log(`Servidor iniciado na porta ${PORT}`);
});
