# Power Shell script para gerar certificado (Alternativa para Windows)
$SSL_DIR = "..\nginx\ssl"
if (!(Test-Path $SSL_DIR)) {
    New-Item -ItemType Directory -Force -Path $SSL_DIR | Out-Null
}

Write-Host "Gerando certificado autossinado para o Nginx..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $SSL_DIR\key.pem -out $SSL_DIR\cert.pem -subj "/C=BR/ST=SP/L=Atibaia/O=UniFAAT/OU=IT/CN=localhost"

Write-Host "Certificados gerados com sucesso."
