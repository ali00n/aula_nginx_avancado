# Configurações do Nginx

Este documento descreve detalhadamente as configurações avançadas implementadas no Nginx do nosso projeto TF04.

## 1. Otimização e Compressão (GZIP)
Ativamos o Gzip para reduzir o consumo de rede no envio de estáticos e json, acelerando severamente os retornos na web.
```nginx
    gzip  on;
    gzip_vary on;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript;
```

## 2. Logs Estruturados de Upstream
Customizamos o Logger para mostrar a visibilidade de onde a requisição encostou em nossa Load Balancer Pool, isso é importante para auditoria.
Criou-se a variável `$upstream_addr` acompanhando qual foi o container de backend engatado, e a variável de `$upstream_response_time`.

## 3. Segurança (Rate Limiting)
Em `nginx.conf`, definimos limitações cruciais de conexão para frear intenções abusivas DDOS numa chave de zona batizada `mylimit` (10MB e 10 reqs limit/seg undo).
Posteriormente atrelamos o `limit_req` apenas na área da API (`location /api/`) por possuir custo de infra, com a regra de "burst", ou seja, os clientes podem ultrapassar muito brevemente essa cota de segurança mas em geral são podados com 503 limit_req nodelay.

## 4. HTTPS (Terminação SSL)
Todo tráfego HTTP porta 80 está rodando um redirecionamento forçado para a 443 do host:
```nginx
    listen 80;
    return 301 https://$host$request_uri;
```
Na porta 443 configurou-se os caminhos do `cert` e `key` criados com uso do script OpenSSL nativo do Linux. Foram desativados suites fracos (apenas configurados TLSv1.2 e 1.3).

## 5. Endpoints Virtuais Baseados no Roteamento
- `/`: proxy para o Frontend do Web Server virtual estático no seu sub-container em `:80`
- `/api/`: proxy para o Bloco Upstream do balanceamento
- `/admin/`: Aplicação de reescrita (regex que extingue o `/admin/` para que o conteiner do painel entregue sem saber que está rodando debaixo desse proxy path).
- `/nginx-status`: Acesso bruto do metadado de conexões.
