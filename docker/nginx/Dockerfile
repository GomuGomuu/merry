FROM nginx:1.22-alpine

ARG NGINX_HOST_PORT
ARG LOCAL_DOMAIN

# Instala o OpenSSL
RUN apk add --no-cache openssl

# Gera certificados autoassinados
RUN openssl req -x509 -nodes -days 365 \
-subj "/C=CA/ST=QC/O=Company, Inc./CN=${LOCAL_DOMAIN}:4${NGINX_HOST_PORT}" \
-addext "subjectAltName=DNS:*.${LOCAL_DOMAIN}:4${NGINX_HOST_PORT}" \
-newkey rsa:2048 \
-keyout /etc/nginx/privkey.pem \
-out /etc/nginx/cert.pem

# Copia o arquivo de configuração do Nginx
COPY ./docker/nginx/merry.conf.template /etc/nginx/templates/
