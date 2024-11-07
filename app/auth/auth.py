from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


# Função para criar o token JWT
def criar_token(identidade):
    return create_access_token(identity=identidade)


# Função para pegar a identidade do usuário a partir do token JWT
def pegar_identidade():
    return get_jwt_identity()


jwt_required()
