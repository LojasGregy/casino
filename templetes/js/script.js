// Script.js

// Função para mostrar e ocultar o menu lateral
function toggleSideMenu() {
    var sideMenu = document.getElementById('sideMenu');
    sideMenu.classList.toggle('active');
}

// Função para alternar o modo escuro
function toggleDarkMode() {
    var body = document.body;
    body.classList.toggle('dark-mode');
}

// Adiciona um evento de clique ao botão de alternar menu lateral
document.getElementById('toggleMenuBtn').addEventListener('click', toggleSideMenu);

// Adiciona um evento de clique ao botão de alternar modo escuro
document.getElementById('toggleDarkModeBtn').addEventListener('click', toggleDarkMode);
