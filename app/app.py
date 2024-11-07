from flask import Flask, jsonify, make_response
from models import db, Usuarios, Clube
from config.config import Config
from auth.auth import criar_token, jwt_required, pegar_identidade
from auth import jwt

app = Flask(__name__)

app.config.from_object(Config)  # instanciar as configurações do sistema
jwt.init_app(app)
db.init_app(app)  # Inicializar o banco de dados
with app.app_context():
    db.create_all()  # Caso não tenha criado criar as tabelas do banco


@app.route('/<nome>/<username>/<senha>/', methods=['GET', 'POST'])
def cadastro_usuario(nome: str, username: str, senha: str):
    usuario = Usuarios(nome=nome, username=username)
    usuario.set_senha(senha)
    db.session.add(usuario)
    db.session.commit()
    return 'Usuario Cadastrado'


@app.route('/login/<username>/<senha>', methods=['GET'])
def login(username: str, senha: str):
    usuario = Usuarios.query.filter_by(username=username).first()
    validacao = Usuarios.checar_senha(usuario.hash_senha, senha)
    if usuario and validacao:
        token = criar_token(identidade=usuario.username)
        response = make_response(jsonify({'user': usuario.username, 'login': usuario.hash_senha, 'token': token}))
        response.set_cookie('JWT_TOKEN', token, httponly=True, secure=True)
        return response
    return jsonify({'status': 'Falha'})


@app.route('/atualizar/nome=<nome>', methods=['GET', 'POST'])
@app.route('/atualizar/username=<username>', methods=['GET', 'POST'])
@app.route('/atualizar/senha=<senha>', methods=['GET', 'POST'])
@jwt_required()
def atualizar(nome=None, username=None, senha=None):
    # Obter a identidade do usuário autenticado
    identidade_usuario = pegar_identidade()

    usuario = Usuarios.query.filter_by(username=identidade_usuario).first()

    if usuario is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    try:
        if nome is not None:
            usuario.nome = nome
        elif username is not None:
            usuario.username = username
        else:
            usuario.hash_senha = Usuarios.gerar_hash(senha)
        db.session.commit()
        return jsonify({"mensagem": "Dados atualizados com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/deletar', methods=['GET'])
@jwt_required()
def deletar():
    # Obter a identidade do usuário autenticado
    identidade_usuario = pegar_identidade()
    # Buscar o usuário no banco de dados e verifica se ele existe
    usuario = Usuarios.query.filter_by(username=identidade_usuario).first()
    if usuario is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    try:
        # Remover o usuário encontrado
        db.session.delete(usuario)
        db.session.commit()

        return jsonify({"message": "Usuario excluido com sucesso"}), 200
    except Exception as e:
        # Caso haja um erro, faz rollback e retorna o erro
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/clube/<nome>')
@jwt_required()
def cadastra_clube(nome):
    clube = Clube(nome_clube=nome)
    db.session.add(clube)
    db.session.commit()
    return 'Clube Cadastrado'


@app.route('/atualizar_clube/<nome_clube>/<novo_nome>')
@jwt_required()
def atualizar_clube(nome_clube, novo_nome):
    clube = Clube.query.filter_by(nome_clube=nome_clube).first()
    clube.nome_clube = novo_nome
    db.session.commit()
    return 'Atualizado'


@app.route('/deletar_clube/<nome_clube>')
@jwt_required()
def deletar_clube(nome_clube):
    clube = Clube.query.filter_by(nome_clube=nome_clube).first()
    db.session.delete(clube)
    db.session.commit()
    return 'Deletado'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
