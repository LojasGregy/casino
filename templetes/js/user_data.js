$(document).ready(function() {
    // Função para carregar os dados do usuário via AJAX
    function loadUserData() {
        $.ajax({
            url: '/get_user_data', // Rota no servidor Flask para obter os dados do usuário
            method: 'GET',
            success: function(data) {
                // Atualiza dinamicamente o conteúdo do painel do usuário com os dados recebidos
                displayUserData(data);
            },
            error: function(error) {
                console.error('Erro ao obter os dados do usuário:', error);
            }
        });
    }

    // Função para exibir os dados do usuário no painel
    function displayUserData(userData) {
        // Atualiza o conteúdo do painel do usuário com os dados recebidos
        $('#userDashboard').html(`
            <p>Nome de Usuário: ${userData.username}</p>
            <p>Email: ${userData.email}</p>
            <p>Saldo: ${userData.saldo}</p>
            <!-- Adicione mais campos conforme necessário -->
        `);
    }

    // Carrega os dados do usuário quando a página é carregada
    loadUserData();
});
