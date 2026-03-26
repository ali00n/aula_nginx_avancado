# TF04 - E-commerce com Load Balancer Avançado

## Aluno
- **Nome:** [ALISSON RIBEIRO ALMEIDA]
- **RA:** [6324605]
- **Curso:** Análise e Desenvolvimento de Sistemas 5° semestre

## Arquitetura
- **Nginx:** Load balancer principal, configurado para SSL, Rate Limiting, compressão GZIP e Logs Detalhados com Upstream Info.
- **Backend:** 3 instâncias da API (Python/Flask) distribuídas via algoritmo `least_conn`. Duas instâncias de "stress": um simula de forma leve uma demora na rede, o outro simula ocasionais falsos negativos de API ressaltando o valor dos health checks e a failover.
- **Frontend:** Loja virtual estática desenvolvida com HTML/CSS, e Javascript para comunicação com a API (consumindo /api/info e /api/produtos).
- **Admin:** Painel administrativo estático oferecendo requisições massivas para verificar a distribuição de carga no browser.

## Funcionalidades Implementadas
- Load balancing com algoritmo `least_conn`
- Health checks automáticos (`max_fails` e `fail_timeout`)
- Failover transparente tolerante a falhas
- SSL/TLS com certificado self-signed configurado
- Rate limiting para proteção da API (`limit_req_zone`)
- Logs detalhados com informações customizadas de upstream
- Compressão Gzip ativada para HTML/CSS/JS/JSON
- Virual hosts usando URI-based routing (Admin Panel vs API vs Frontend)
- Endpoint de métricas Nginx implementado `/nginx-status`

## Como executar

### Pré-requisitos
- docker e Docker Compose instalados no host
- OpenSSL intalado (necessário para os certificados TLS de teste local), ou Bash/Powershell para a execução do script criador de certificados encriptados.

### Execução
```bash
git clone https://github.com/ali00n/aula_nginx_avancado.git
cd aula_nginx_avancado -- caso nao esteja ja na pasta

# Gerar certificados SSL no Windows via Powershell (Alternativa para Windows)
./scripts/generate-ssl.ps1

# Subir todos os serviços rodando em modo Daemon e fazendo as builds de cada conteiner
docker-compose up -d --build

# Verificar status para assegurar que os 5 containers estão funcionais (nginx, frontend, admin, 3x backend)
docker-compose ps
```

### Endpoints (HTTPS está acessível com certificado fake, ignorar o erro de segurança pelo browser, só para fins de teste)
- **Frontend:** http://localhost ou https://localhost
- **API (Root API Infos):** http://localhost/api/info ou https://localhost/api/info 
- **Admin:** http://localhost/admin/ (Sendo um subdiretório roteado dinamicamente para index no painel admin)
- **Status de Métricas Engine (Nginx):** http://localhost/nginx-status
- **Health Check Nativo da App:** http://localhost/health (Redirecionado para api_backend/health)

## Testes de Load Balancing

### 1- Testar distribuição natural pela Carga das 3 Instâncias
```bash
for i in {1..10}; do
  curl -s http://localhost/api/info | grep instance_id
done
```

### 2- Simular falha grave paralisando o funcionamento de Node 1 (backend1)
```bash
docker stop ecommerce-backend1
# Em seguida, enviar requisição de novo e verificar que o Nginx excluiu ele automaticamente devido à failover e ao least_conn.
curl http://localhost/api/info
```

## Monitoramento

- **Logs detalhados de requisições:** `docker-compose logs nginx`
- **Métricas:** http://localhost/nginx-status
- Os health checks automáticos de failover de rotina são garantidos com diretivas explícitas de tentativas (escala 30s de check via erro do timeout).

## Links de Documentações Auxiliares do Projeto:
- **Detalhes de Load Balance:** [Load Balancing Specs](./docs/load-balancing.md)
- **Detalhes de Setup do Nginx e Hardening:** [Nginx Config Specs](./docs/nginx-config.md)

Desenvolvido por: Alisson Ribeiro Almeida
Última atualização: 26/03/2026

# ESTRUTURA DO PROJETO

NGINX_AVANCADO/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── config.py
│   └── logger.py
├── frontend/
│   ├── index.html
│   ├── produtos.html
│   ├── carrinho.html
│   ├── css/
│   │   └── style.css
│   └── Dockerfile
├── admin/
│   ├── dashboard.html
│   └── Dockerfile
├── nginx/
│   ├── nginx.conf
│   ├── conf.d/
│   │   ├── load-balancer.conf
│   │   └── ssl.conf
│   └── ssl/
│       ├── cert.pem
│       └── key.pem
├── scripts/
│   ├── generate-ssl.ps1
│   └── generate-ssl.sh
├── docs/
│   ├── load-balancing.md
│   └── nginx-config.md
└── docker-compose.yml
