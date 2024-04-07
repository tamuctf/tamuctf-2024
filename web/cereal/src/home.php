<?php
require_once('config.php');

// Check if logged in
if (!isset($_COOKIE['auth']) || empty($_COOKIE['auth'])) {
	header('Location: logout.php');
	exit;
}

$cookie = unserialize(base64_decode($_COOKIE['auth']));

?>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Home Page</title>
		<link href="static/style.css" rel="stylesheet" type="text/css">
	</head>
	<body class="loggedin">
		<nav class="navtop">
			<div>
				<h1>Website Title</h1>
				<a href="profile.php"><i class="fas fa-user-circle"></i>Profile</a>
				<a href="logout.php"><i class="fas fa-sign-out-alt"></i>Logout</a>
			</div>
		</nav>
		<div class="content">
			<h2>Home Page</h2>
			<p>Welcome back, user!</p>
		</div>
	</body>
</html>

