<?php
require_once('config.php');

// Checking if data was sent in POST request
if ( !isset($_POST['username'], $_POST['password']) ) {
	exit('Please fill both the username and password fields!');
}

if ( !is_file('../important.db') ) {
	exit('Server error: database missing!');
}

// POST request variables
$username=$_POST['username'];
$password=$_POST['password'];

// Database connection
$conn = new PDO('sqlite:../important.db');
$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$query = "select * from users where `username` = :username AND `password` = :password";
$stmt = $conn->prepare($query);
$stmt->bindParam(':username', $username);
$stmt->bindParam(':password', $password);
$stmt->execute();
$row = $stmt->fetch();

// Creating cookie
if ($row['username'] === $username && $row['password'] === $password) {
	$cookie_name='auth';
	$cookie = new User();
	$cookie->username = $username;
	$cookie->id = (int)$row['id'];
	$cookie->setPassword(md5($row['password']));
	setcookie($cookie_name, base64_encode(serialize($cookie)), time() + (86400 * 30), "/");
	echo 'Welcome ' . $username . '! ' . '<br><br><a href="home.php"><i class="fas fa-user-circle"></i>Home</a>';
} else {
	// Incorrect password
	echo 'Incorrect username and/or password!';
}

?>
