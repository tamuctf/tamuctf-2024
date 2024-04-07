<?php
if (isset($_COOKIE['auth'])) {
    unset($_COOKIE['auth']); 
    setcookie('auth', '', -1, '/'); 
}
// Back to login you go
header('Location: index.html');
?>
