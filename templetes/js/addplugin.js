function addPlugin() {
    var pluginName = document.getElementById('pluginName').value;
    var pluginJSUrl = document.getElementById('pluginJSUrl').value;
    var pluginCSSUrl = document.getElementById('pluginCSSUrl').value;

    // Cria um elemento <script> para incluir o arquivo JavaScript do plugin
    var scriptElement = document.createElement('script');
    scriptElement.src = pluginJSUrl;
    document.body.appendChild(scriptElement);

    // Cria um elemento <link> para incluir o arquivo CSS do plugin
    var linkElement = document.createElement('link');
    linkElement.rel = 'stylesheet';
    linkElement.type = 'text/css';
    linkElement.href = pluginCSSUrl;
    document.head.appendChild(linkElement);

    // Adiciona uma mensagem na página para indicar que o plugin foi adicionado com sucesso
    var messageElement = document.createElement('div');
    messageElement.textContent = 'Plugin ' + pluginName + ' adicionado com sucesso!';
    document.body.appendChild(messageElement);
}
