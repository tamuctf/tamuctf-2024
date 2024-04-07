<?php
include 'config.php';
include 'bulletproof.php';

function random_filename($length, $directory = '', $extension = '')
{
    // default to this files directory if empty...
    $dir = !empty($directory) && is_dir($directory) ? $directory : dirname(__FILE__);

    do {
        $key = '';
        $keys = array_merge(range(0, 9), range('a', 'z'));

        for ($i = 0; $i < $length; $i++) {
            $key .= $keys[array_rand($keys)];
        }
    } while (file_exists($dir . '/' . $key . (!empty($extension) ? '.' . $extension : '')));

    return $key . (!empty($extension) ? '.' . $extension : '');
}

session_start();
$sess = basename(session_id());

if($sess !== session_id()) {
  echo "ERROR: Invalid session cookie. Please delete the PHPSESSID cookie.";
  die();
}

if(!file_exists('/tmp/uploads/' . $sess)) {
  mkdir('/tmp/uploads/' . $sess, 0755, true);
}

if($_SERVER['REQUEST_METHOD'] === 'POST') {
  if(isset($_FILES['toUpload'])) {
    $image = new Bulletproof\Image($_FILES);
    if($image['toUpload']) {
      $image->setLocation("/tmp/uploads/" . $sess);
      $image->setSize(100, 3000000);
      $image->setMime(array('jpeg', 'gif', 'png'));
      $upload = $image->upload();
  
      if($upload) {
        header('Location: /index.php?message=Image uploaded successfully&status=success');
      } else {
        header('Location: /index.php?message=Image upload failed&status=fail');
      }
    } else {
      header('Location: /index.php?message=Image upload failed&status=fail');
    }
  } else if(isset($_REQUEST['url'])) {
    if(!preg_match("/(htm)|(php)|(js)|(css)/", $_REQUEST['url'])) {
      $url = filter_var($_REQUEST['url'], FILTER_SANITIZE_URL);
      if(filter_var($url, FILTER_VALIDATE_URL)) {
        $img = file_get_contents($url); 
        if($img !== false) {
          $mime = substr($url, strrpos($url, '.') + 1);
          $file = random_filename(32, '/tmp/uploads/' . $sess, $mime);
          
          $f = fopen('/tmp/uploads/' . $sess . '/' . $file, "wb");
          if($f !== false) {
            fwrite($f, $img);
            fclose($f);
            header('Location: /index.php?message=Image uploaded successfully&status=success');
          } else {
            header('Location: /index.php?message=Image upload failed&status=fail'); 
          }
        } else {
          header('Location: /index.php?message=Image upload failed&status=fail');
        }
      } else {
        header('Location: /index.php?message=Image upload failed&status=fail');
      }
    } else {
      header('Location: /index.php?message=Image upload failed&status=fail');
    }
  }
} else {
  if(isset($_GET['file'])) {
    $safe = basename($_GET['file']);
    if($safe !== "" && file_exists('/tmp/uploads/' . $sess . "/" . $safe)) {
      $file = '/tmp/uploads/' . $sess . "/" . $safe;
      $fp = fopen($file, 'rb');

      header('Content-Type: '. mime_content_type($file));
      header('Content-Length: ' . filesize($file));

      fpassthru($fp);
      die();
    } else {
      header('Location: /index.php?message=File not found&status=fail');
    }
  }
}
?>

<!DOCTYPE html>
<html>
<head>
<title>Definitely Not Google Drive</title>
<link href='static/style.css' rel='stylesheet'>
</head>
<body>
<div class=header>
  <div class=title>
    <h1>Definitely Not Google Drive</h1>
  </div>
</div>
<div class=page>
  <div class=content>
    <form class="image-upload-form" enctype="multipart/form-data" method="POST" action="/">
      <div class="file-select">
        <div class="upload-bar">
          <div class="file-select-btn" id="fileName">
            Choose File
            <input type="file" accept="image/png,image/jpeg,image/gif" name="toUpload" id="chooseFile" required>
          </div>
          <div class="file-select-name" id="noFile">
            <input type="text" placeholder="No file chosen..." id="url">
          </div>
        </div>
        <div class="submit">
          <p>Upload</p>
          <input type="submit" value="Submit">
        </div>
      </div>
      <div class="result" id="result">
      </div>
    </form>
    <div class=image-display>
<?php
if(scandir('/tmp/uploads/' . $sess) != False) {
  $files = array_diff(scandir('/tmp/uploads/' . $sess), array('.', '..'));

  foreach($files as &$f) {
    echo "<a href=/index.php?file=" . $f . "><div class=card><img class=thumbnail src=/index.php?file=" . $f . "></div></a>";
  }
}
?>
    </div>
  </div>
</div>
  <script src="static/jquery/jquery.min.js"></script>
  <script>
    (function ($) {
      $('#chooseFile').bind('change', function() {
        var filename = $('#chooseFile').val();
        if(/^\s*$/.test(filename)) {
          $('.upload-bar').removeClass('active');
          $('#noFile').text("No file chosen...");
        } else {
          $('.upload-bar').addClass('active');
          $('#noFile').text(filename.replace("C:\\fakepath\\", ""));
        }
      });

      $('#url').bind('change', function() {
        document.getElementById('chooseFile').required = false;
        $('.upload-bar').addClass('active');
      });
    })(window.jQuery);
  </script>
  <script>
    const params = new URLSearchParams(window.location.search);
    if(params.has('message') && params.has('status')) {
      if(params.get('status') == 'success') {
        document.getElementById("result").style.color = '#3fa46a';
        document.getElementById("result").innerText = params.get('message');
      } else {
        document.getElementById("result").style.color = '#dc3545';
        document.getElementById("result").innerText = params.get('message');
      }
    }
  </script>
  <script>
    document.querySelector('form').addEventListener('submit', async function(event) {  
      const form = event.currentTarget;
      const url = new URL(form.action);

      if(document.getElementById('noFile').innerHTML.trim() == '<input type="text" placeholder="No file chosen..." id="url">') {
        event.preventDefault();

        let response = await fetch('/index.php', {
          method: "POST",
          headers: {
            "Content-Type":"application/x-www-form-urlencoded"
          },
          body: "url=" + document.getElementById('url').value
        });

        let redir = await response.url;
        window.location.href = redir;
      }
    });
  </script>
</body>
</html>
