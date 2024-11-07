import os
from datetime import timedelta


class Config:
    # A chave secreta é usada para proteger sessões e cookies gerados pelo Flask.
    # A chave secreta deve ser mantida em segredo e nunca deve ser compartilhada publicamente.
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24).hex())

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', os.urandom(24).hex())

    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', timedelta(hours=1))

    JWT_TOKEN_LOCATION = 'cookies'

    JWT_ACCESS_COOKIE_NAME = 'JWT_TOKEN'

    # Define se o modo de depuração está ativado.
    # O modo de depuração deve ser desativado em produção para evitar vazamentos de informações sensíveis.
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)  # Use variáveis de ambiente para controlar o modo de depuração.

    # Configurações do banco de dados

    # Define a URI do banco de dados para MySQL.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             'mysql+mysqlconnector://root:teste@localhost:3306/teste')

    # Define se as modificações no banco de dados devem ser rastreadas. Isso ajuda no controle de versão do banco de
    # dados.
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS',
                                                    True)  # Desative para evitar avisos de desempenho.

    # Define se os modelos devem ser recarregados automaticamente sempre que forem modificados.
    # Isso é útil durante o desenvolvimento, mas deve ser desativado em produção para melhorar o desempenho.
    TEMPLATES_AUTO_RELOAD = os.environ.get('TEMPLATES_AUTO_RELOAD', True)
