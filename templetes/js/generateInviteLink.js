// Função para gerar um link de convite
function generateInviteLink() {
    // Aqui você pode gerar um código único para o link de convite, por exemplo, um ID de usuário único ou um código aleatório
    var inviteCode = generateUniqueCode(); // Função fictícia para gerar um código único

    // Aqui você pode montar o link de convite com base no código gerado
    var inviteLink = window.location.origin + '/signup?invite=' + inviteCode;

    // Exibe o link de convite gerado
    document.getElementById("inviteLink").innerHTML = inviteLink;
}

// Função fictícia para gerar um código único
function generateUniqueCode() {
    // Aqui você pode implementar a lógica para gerar um código único, por exemplo, um código aleatório ou um ID de usuário único
    return 'ABC123'; // Exemplo de código único
}
