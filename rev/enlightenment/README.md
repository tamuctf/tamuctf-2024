# Enlightenment

Author: `Addison`

Sometimes, it's nice to just listen and observe.

## Solution

When the binary runs it seems to do nothing, but stracing and waiting two minutes reveals that it makes a network connection. Listening to this connection with wireshark reveals that the binary is reaching out to `cdn.discordapp.com`. Since the request is being made over SSL, the request data isn't trivially readable. To be able to view the request content, we must trick the binary into sending the request to localhost.

The first step is to generate an SSL cert using openssl and setup an nginx server to listen.

`sudo openssl req -x509 -newkey rsa:2048 -keyout /etc/ssl/private/nginx.pem -out /etc/ssl/certs/nginx.crt -nodes`

When making the certificates, the FQDN must be set to `cdn.discordapp.com`.

```nginx
server {
    listen 80;
    listen [::]:80;
    return 301 https://$host$request_uri;
}

server {
    listen 443 http2 ssl;
    listen [::]:443 http2 ssl;

    ssl_certificate /etc/ssl/certs/nginx.crt;
    ssl_certificate_key /etc/ssl/private/nginx.pem;
    ssl_dhparam /etc/ssl/certs/dhparam.pem;

    ssl_protocols TLSv1.3;# Requires nginx >= 1.13.0 else use TLSv1.2
    ssl_prefer_server_ciphers on;
    ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
    ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
    ssl_session_timeout  10m;
    ssl_session_cache shared:SSL:10m;
    ssl_session_tickets off; # Requires nginx >= 1.5.9
    ssl_stapling on; # Requires nginx >= 1.3.7
    ssl_stapling_verify on; # Requires nginx => 1.3.7
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
    # Disable preloading HSTS for now.  You can use the commented out header line that includes
    # the "preload" directive if you understand the implications.
    #add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";

    root /usr/share/nginx/html;

    location / {
    }

    error_page 404 /404.html;
	location = /404.html {
    }

    error_page 500 502 503 504 /50x.html;
    	location = /50x.html {
    }
}
```

Once nginx is running, the openssl `SSL_CERT_FILE` environment variable can be set so that the certificate is trusted. Finally, the `/etc/hosts` file needs to route `cdn.discordapp.com` to `127.0.0.1`.

The request will show up in `/var/log/nginx/access.log`.

`127.0.0.1 - - [23/Mar/2024:02:58:24 -0500] "GET /attachments/1098492589256233000/1220991491841724456/c2c98fd47cd48ae3b6687a7ded56ac347b3f965dcf87874b2bfbec55b6026bc437c2d5673b5e4fbe1a6a55270ac0b3972f19fe62b66c225831ba0a5bb470a716?ex=6610f3f0&is=65fe7ef0&hm=cadd5e9158fde45665a31a0c04cc6f77181611c5599045532a9d2f5b0650ab65& HTTP/1.1" 404 153 "-" "-"`

Navigating to this file on Discord's CDN provides the flag as shown below.

Flag: `gigem{7ru5t_n0_0n3_n07_3veN_yourself}`
