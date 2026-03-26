#!/bin/bash

# Diretorios
SSL_DIR="../nginx/ssl"
mkdir -p $SSL_DIR

echo "Gerando certificado autossinado para o Nginx..."

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout $SSL_DIR/key.pem \
  -out $SSL_DIR/cert.pem \
  -subj "/C=BR/ST=SP/L=Atibaia/O=UniFAAT/OU=IT/CN=localhost"

echo "Certificados gerados em $SSL_DIR"
