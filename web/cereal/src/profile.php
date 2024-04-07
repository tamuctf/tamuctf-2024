<?php
require_once('config.php');

// Check if logged in
if (!isset($_COOKIE['auth']) || empty($_COOKIE['auth'])) {
	header('Location: logout.php');
	exit;
}

$cookie = unserialize(base64_decode($_COOKIE['auth']));
$row = $cookie->sendProfile();

$username = $row[0];
$email = $row[1];
$cereal = $row[2];
$date = date('Y-m-d H:i:s', $row[3]);

?>

<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>Profile Page</title>
		<link href="static/style.css" rel="stylesheet" type="text/css">
	</head>
	<body class="loggedin">
		<nav class="navtop">
			<div>
				<h1>Website Title</h1>
				<a href="home.php"><i class="fas fa-user-circle"></i>Home</a>
				<a href="logout.php"><i class="fas fa-sign-out-alt"></i>Logout</a>
			</div>
		</nav>
		<div class="content">
			<h2>Profile Page</h2>
			<div>
				<p>Your account details are below:</p>
				<table>
					<tr>
						<td>Username:</td>
						<td><?=htmlspecialchars($username, ENT_QUOTES)?></td>
					</tr>
					<tr>
						<td>Email:</td>
						<td><?=htmlspecialchars($email, ENT_QUOTES)?></td>
					</tr>
					<tr>
						<td>Account Creation Date:</td>
						<td><?=htmlspecialchars($date, ENT_QUOTES)?></td>
					</tr>
					<tr>
						<td>Favorite Cereal:</td>
						<td><?=htmlspecialchars($cereal, ENT_QUOTES)?></td>
					</tr>
				</table>
			</div>
		</div>
	</body>
</html>
