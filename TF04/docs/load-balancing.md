# Tolerância a falhas e Balanceamento de Carga

## Filosofia de Load Balance: `least_conn`
O padrão original round_robin não se aplica em sistemas assimétricos. Uma API pode demorar e ficar ocupada, não fazia sentido encaminhar a próxima para essa instância ocupada.
Desta forma optamos pela tag `least_conn`. O Nginx ativamente encaminha para o worker onde há MENOS canais de escuta engrenados no ato, maximizando eficiência.
Para constatar esse conceito de instâncias com diferentes graus, injetamos DELAYS em uma das imagens no docker-compose para que essa lentidão provasse ao proxy engolir a rota que não ia preferençar ela.

## Health Checks Naturais do Proxy (Failover Automático)
O Upstream foi parametrizado explicitamente:
```nginx
server backend1:5000 max_fails=3 fail_timeout=30s;
server backend2:5000 max_fails=3 fail_timeout=30s;
...
```
- Failover e Fail Tolerances: O Nginx monitora silenciosamente os erros HTTP de rede (Conexões recusadas). Se a Aplicação gerar falhas durantes essas passagens ele soma ao flag de max fails. 
Batendo de frente aos 3 MAX_FAILS, a rota é considerada "unhealthy" e não toma mais passagens por um prazo de **30 Segundos**. Depois de 30 ciclos de espera o proxy volta a enxergar chance de vida e injeta pacote pra ver se a máquina reviveu.

## Monitoramento da Saúde
Implementou-se no código da API do Flask (no `/health`) para validar manualmente o status interno dele, caso se aplique. Como o sistema de e-commerce é dinâmico, também é validado.
