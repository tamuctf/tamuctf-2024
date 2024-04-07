FROM php:7.2-apache

COPY src/ /var/www/html

ARG flag
ARG port
# added to make it read-able but not writeable (someone might have deleted it)
RUN echo ${flag} >> /var/www/flag-de88df3ebf2f0c4bf871ddfb2e0fcce4.txt && \
    chmod 444 /var/www/flag-de88df3ebf2f0c4bf871ddfb2e0fcce4.txt && \
    mkdir /tmp/uploads && \
    chown www-data:www-data /tmp/uploads &&\
    chmod 444 /var/www/html/*.php && \
    sed -i 's@Listen 80@Listen '"${port}"'@g' /etc/apache2/ports.conf && \
    sed -i 's@\*:80@\*:'"${port}"'@g' /etc/apache2/sites-enabled/000-default.conf && \
    sed -i 's@#Include conf-available/serve-cgi-bin.conf@<Location /uploads>\nrequire all granted\n</Location>\nAlias /uploads "/tmp/uploads"@g' /etc/apache2/sites-enabled/000-default.conf && \
    docker-php-ext-install exif
