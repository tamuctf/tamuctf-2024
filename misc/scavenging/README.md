# Scavenging

Author: `Addison`

Look around, see what you can find!

Note: File uploads for this challenge are not necessary; you can complete it with the binaries provided.

## Solution

```sh
(
  head -n 1;
  sleep 5;
  echo 'mount -t devtmpfs dev dev';
  sleep .1;
  echo 'xxd -s 1048576 /dev/mem | xxd -r -p | grep gigem';
  read
) | nc localhost 5000
```

Flag: `gigem{now_where_did_that_come_from_exactly}`
