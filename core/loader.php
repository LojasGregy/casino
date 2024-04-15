<?php

// Definição do namespace para as Lojas Gregy
define("LOJAS_GREGY_NAMESPACE", "LojasGregy");

// Função de autoload para carregar as classes automaticamente
spl_autoload_register(function ($className) {
    // Caminho para a classe
    $classPath = $_SERVER["DOCUMENT_ROOT"] . '/core/classes/' . $className . '.class.php';

    // Verifica se o arquivo da classe existe
    if (file_exists($classPath)) {
        // Inclui o arquivo da classe
        require_once($classPath);
    }
});

?>
