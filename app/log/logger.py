import logging
from flask import request


logging.basicConfig(
    filename='log/acess.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='UTF-8'
)



def info_log():
    logging.debug(f"Headers: {request.headers}")
    logging.info(f"Requisição para {request.path} com método {request.method}")
    logging.debug(f"Dados: {request.get_data(as_text=True)}")



def resposta_log(response):
    logging.info(f"Resposta com status {response.status}", )
    logging.debug(f"Dados de resposta: {response.get_data(as_text=True)}", )
    return response
