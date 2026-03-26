from flask import Flask, jsonify, request
import os
import socket
import time
import random
from logger import CustomLogger


logger = CustomLogger()

app = Flask(__name__)

# Configurações a partir de variáveis de ambiente ou com valores padrão
INSTANCE_ID = os.environ.get('INSTANCE_ID', socket.gethostname())
DELAY_SIMULATION = float(os.environ.get('DELAY_SIMULATION', 0.0))

@app.route('/api/info')
def info():
    """Retorna informações da instância para constatar o balanceamento de carga"""
    logger.log("info", "Recebendo requisicao de informacoes", "INICIADO")
    
    if DELAY_SIMULATION > 0:
        logger.log("info", f"Simulando lentidao de {DELAY_SIMULATION}s", "AGUARDANDO")
        time.sleep(DELAY_SIMULATION)
        
    logger.log("info", "Retornando dados da instancia", "SUCESSO")
    return jsonify({
        "status": "online",
        "instance_id": INSTANCE_ID,
        "message": "Requisição processada com sucesso !",
        "timestamp": time.time()
    })

@app.route('/api/produtos')
def produtos():
    """Retorna uma lista fictícia de produtos"""
    logger.log("produtos", "Buscando lista de produtos", "INICIADO")
    
    produtos_list = [
        {"id": 1, "nome": "Notebook Pro", "preco": 5499.00, "descricao": "Processador rápido, 16GB RAM"},
        {"id": 2, "nome": "Smartphone Max", "preco": 3299.00, "descricao": "Câmera 108MP, Bateria longa duração"},
        {"id": 3, "nome": "Fone Wireless", "preco": 299.00, "descricao": "Cancelamento de ruído ativo"},
        {"id": 4, "nome": "Monitor UltraWide", "preco": 1899.00, "descricao": "29 polegadas, 75Hz"},
        {"id": 5, "nome": "Teclado Mecânico", "preco": 450.00, "descricao": "Switches Red, RGB"}
    ]
    
    logger.log("produtos", f"Retornando {len(produtos_list)} produtos", "SUCESSO")
    return jsonify({
        "instance_id": INSTANCE_ID,
        "produtos": produtos_list
    })

@app.route('/health')
def health_check():
    """Endpoint customizado de health check para o Nginx"""
    logger.log("health_check", "Verificando integridade da aplicacao", "INICIADO")
    
    # Simula possibilidade de falha para testes (1% de chance de erro 500 para testes avançados)
    if os.environ.get('SIMULATE_FAILURE', 'false').lower() == 'true':
        if random.random() < 0.05:
            logger.log("health_check", "Falha simulada alcancada", "ERRO_500")
            return jsonify({"status": "error", "message": "Simulated failure"}), 500
            
    logger.log("health_check", "Instancia saudavel", "SUCESSO")
    return jsonify({"status": "healthy", "instance": INSTANCE_ID}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
