# backend logger // por mais que nao esteja visivel para o cliente achei interessante implementar
# tanto para estudos quanto para entendimento da aplicação

# nao achei necessario criar uma classe para uma só função se torna redundante, mas
# para fins de estudo e organização do código achei válido

import sys
from datetime import datetime

class CustomLogger:
    @staticmethod
    def log(function_name: str, action: str, status: str):
        """
        Gera um log customizado e faz o flush para o terminal do Docker/IDE.
        Formato: MAIN | (NOME DA FUNCAO) | O QUE ESTA FAZENDO | STATUS DO ANDAMENTO
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # O prefixo timestamp é bom ter, mas o corpo principal segue sua exigência
        msg = f"MAIN | ({function_name}) | {action} | {status}"
        print(f"[{timestamp}] {msg}")
        sys.stdout.flush() # Importante para aparecer em tempo real no docker logs
