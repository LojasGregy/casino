<?php
       if ($_SERVER['HTTPS_HOST']== 'localhost') {
               // Database for my localhost
               define("DB_HOST", "localhost");      // MySQL Database Host
               define("DB_USER", "root");           // MySQL Username
               define("DB_PASS", "");               // MySQL Password
               define("DB_NAME", "");     // database Name
       } else{
             // Database for public 
             define("DB_HOST", "localhost");   //MySQL Database Host
             define("DB_USER", "replace_use");  // MySQL Username
             define("DB_PASS", "replace_password") //MySQL Password
             define("DB_NAME", "replace_db") // Database Name 
       }
?>
