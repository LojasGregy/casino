<?php

use PSpell\Config;

require_once $_SERVER["DOCUMENT_ROOT"] . '/core/sql.php';
require $_SERVER["DOCUMENT_ROOT"] . '/core/libs/autoload.php';
require_once $_SERVER["DOCUMENT_ROOT"] . '/core/loader.php';

// Instância das classes necessárias
$DataBase = new DataBase();
$User = new User();
$Other = new Other();
$Config = new Config();
$Metamask = new Metamask();

// Configurações do sistema
$Settings = $Config->settings();
$Config->check($Config->api("lojasgregy")["key"]);

// Configurações do site
$root = '/';
$path = $_GET['page'] ?? '';
$port = $Settings["port"];
$sitename = $Settings["name"];
$sitekeywords = $Settings["keywords"];
$siteauthor = 'Lojas Gregy Ltda';
$siteurl = $Settings["url"];
$sitedescription = $sitename . '|' . $Settings["description"];
$metadesc = $Settings["metadesc"];

// Arrays e variáveis relacionadas a recompensas e afiliados
$rewards_amounts = [];
$names_pages = $Config->translation()["names_pages"];
$ranks_name = $Config->translation()["ranks"];
$referral_comission_deposit = $Settings["referralcomission"];
$affiliates_requirement = [];
$affiliates_comission = ['deposit' => $Settings["afcomdeposit"], 'bet' => $Settings["afcombet"]];

// Configurações de banimento e manutenção
$banip_excluded = [];
$ban_excluded = [];
$maintenance_excluded = [];
$bonus_allowed = [];

// Consulta ao banco de dados para recompensas
$DataBase->Query("SELECT * FROM rewards");
$DataBase->Execute();

foreach ($DataBase->ResultSet() as $row) {
    $rewards_amounts[$row["name"]] = floatval($row["reward"]);
}

// Consulta ao banco de dados para requisitos de afiliados
$DataBase->Query("SELECT * FROM referral_requirements");
$DataBase->Execute();

foreach ($DataBase->ResultSet() as $row) {
    $affiliates_requirement[] = floatval($row["req"]);
}

// Outras configurações do sistema
$level_start = $Settings["levelstart"];
$level_next = $Settings["levelnext"];
$maintenance = $Settings['maintenance'];
$maintenance_message = $Settings['maintenance_message'];

// Definições das redes sociais
$link_steam = $Settings["Steam"];
$link_twitter = $Settings["twitter"];
$link_facebook = $Settings["facebook"];
$link_telegram = $Settings["telegram"];
$link_discord = $Settings["discord"];
$link_instagram = $Settings["instagram"];
$link_tiktok = $Settings["tiktok"];
$link_kwai = $Settings["kwai"];
$link_youtube = $Settings["youtube"];

// Verificação dos vínculos do usuário
$user_binds = array('google' => false , 'facebook'=> false, 'steam' => false );
if(isset($user['userid'])) {
    foreach ($Config->bind($user['userid']) as $key => $value) {
        $user_binds[$value['bind']] = true;
    }
}

// Definições de recompensas e afiliados
$rewards['amounts'] = $rewards_amounts;
$affiliates['requirement'] = $affiliates_requirement;
$affiliates['commission'] = $affiliates_commission;

// Definições do perfil do usuário
$profile['binds'] = $user_binds;
if(isset($user['userid'])) {
    $profile['bet'] = $Config->bet()['bet'];
    $profile['win'] = $Config->win()['win'];
    $profile['have_supports'] = $Config->support()['countSupports'];
    $profile['bets'] = $Config->bets()['bets'];    
} else {
    $profile['bet'] = 0;
    $profile['win'] = 0;
    $profile['have_supports'] = 0;
    $profile['bets'] = 0;
}

// Obtenção do endereço IP do cliente
$ipAddress = !empty($_SERVER['HTTP_CLIENT_IP']) ? $_SERVER['HTTP_CLIENT_IP'] : (!empty($_SERVER['HTTP_X_FORWARDED_FOR']) ? $_SERVER['HTTP_X_FORWARDED_FOR'] : $_SERVER['REMOTE_ADDR']);
$ip = explode(',', $ipAddress)[0];
$ip = trim($ip);

// Configurações do site
$site['root'] = $root;
$site['port'] = $port;
$site['recaptcha'] = $Config->api("recaptcha")["key"];
$site['path'] = $path;
$site['name'] = $sitename;
$site['ip'] = $ip;
$site['keywords'] = $sitekeywords;
$site['author'] = $siteauthor;
$site['url'] = $siteurl;
$site['description'] = $sitedescription;
$site['link_steam'] = $link_steam;
$site['link_twitter'] = $link_twitter;
$site['link_facebook'] = $link_facebook;
$site['link_telegram'] = $link_telegram;
$site['link_discord'] = $link_discord;
$site['link_instagram'] = $link_instagram;
$site['link_tiktok'] = $link_tiktok;
$site['link_kwai'] = $link_kwai;
$site['link_youtube'] = $link_youtube;

$site['ranks_name'] = $ranks_name;
$site['permissions'] = array(
    'banip' => $banip_excluded,
    'ban' => $ban_excluded,
    'maintain' => $maintain_excluded,
    'bonus' => $bonus_allowed
);

?>
