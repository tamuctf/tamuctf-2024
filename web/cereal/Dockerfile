FROM php:7.2-apache

COPY src/ /var/www/html
COPY important.db /var/www

ARG flag
ARG port

RUN chmod 444 /var/www/important.db && \
    sed -i 's@Listen 80@Listen '"${port}"'@g' /etc/apache2/ports.conf && \
    sed -i 's@\*:80@\*:'"${port}"'@g' /etc/apache2/sites-enabled/000-default.conf && \
    chown -R www-data:www-data /var/www/
