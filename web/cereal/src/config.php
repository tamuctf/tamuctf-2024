<?php
class User {
  public $username = '';
	public $id = -1;
	
	protected $password = '';
	protected $profile;

	public function setPassword($pass) {
		$this->password = $pass;
	}

	public function sendProfile() {
		return $this->profile;
	}

	public function refresh() {
		// Database connection
		$conn = new PDO('sqlite:../important.db');
		$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		$query = "select username, email, favorite_cereal, creation_date from users where `id` = '" . $this->id . "' AND `username` = '" . $this->username . "'";
		$stmt = $conn->prepare($query);
		$stmt->execute();
		$row = $stmt->fetch();

		$this->profile = $row;
	}

	public function validate() {
		// Database connection
		$conn = new PDO('sqlite:../important.db');
		$conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
		$query = "select * from users where `username` = :username";
		$stmt = $conn->prepare($query);
		$stmt->bindParam(':username', $this->username);
		$stmt->execute();
		$row = $stmt->fetch();

		if (md5($row['password']) !== $this->password) {
			header('Location: logout.php');
			exit;
		}
	}

	public function __wakeup() {
		$this->validate();
		$this->refresh();
    	}
}

?>
