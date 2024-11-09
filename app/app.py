from flask import Flask, jsonify, make_response, request
from flask_caching import Cache
from models import db, Usuarios, Clube, Livro, Avaliacao
from config.config import Config
from auth.auth import criar_token, jwt_required, pegar_identidade
from auth import jwt
from log.logger import info_log, resposta_log

app = Flask(__name__)
app.config.from_object(Config)  # instanciar as configurações do sistema
cache = Cache(app)
jwt.init_app(app)  # Inicializa a verificação da autenticação
db.init_app(app)  # Inicializar o banco de dados
with app.app_context():
    db.create_all()  # Caso não tenha criado criar as tabelas do banco


@app.before_request
def requisicao_log():
    info_log()


@app.after_request
def responsta_requisicao(responser):
    return resposta_log(responser)


@app.route('/cadastrar', methods=['POST'])
def cadastro_usuario():
    dados = request.get_json()
    usuario = Usuarios(nome=dados['nome'], username=dados['username'])
    usuario.set_senha(dados['senha'])
    db.session.add(usuario)
    db.session.commit()
    return 'Usuario Cadastrado'


@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    usuario = Usuarios.query.filter_by(username=dados['username']).first()
    validacao = Usuarios.checar_senha(usuario.hash_senha, dados['senha'])
    if usuario and validacao:
        token = criar_token(identidade=usuario.username)
        response = make_response(jsonify({'user': usuario.username, 'login': usuario.hash_senha, 'token': token}))
        response.set_cookie('JWT_TOKEN', token, httponly=True, secure=True)
        return response
    return jsonify({'status': 'Falha'})


@app.route('/atualizar', methods=['PUT'])
@jwt_required()
def atualizar():
    dados = request.get_json()
    # Obter a identidade do usuário autenticado
    identidade_usuario = pegar_identidade()

    # Verificar se o usuário existe no banco
    usuario = Usuarios.query.filter_by(username=identidade_usuario).first()

    if usuario is None:
        return jsonify({"error": "Usuário não encontrado"}), 404

    try:
        # Atualizar os dados com base no que foi enviado no JSON
        if 'nome' in dados and dados['nome'] != '':
            usuario.nome = dados['nome']
        elif 'username' in dados and dados['username'] != '':
            usuario.username = dados['username']
        elif 'senha' in dados and dados['senha'] != '':
            usuario.hash_senha = Usuarios.gerar_hash(dados['senha'])

        # Persistir as alterações no banco de dados
        db.session.commit()

        return jsonify({"mensagem": "Dados atualizados com sucesso"}), 200
    except Exception as e:
        # Caso ocorra algum erro, fazer rollback
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/deletar', methods=['DELETE'])
@jwt_required()
def deletar():
    # Obter a identidade do usuário autenticado
    identidade_usuario = pegar_identidade()
    print(identidade_usuario)
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


@app.route('/clube', methods=['POST'])
@jwt_required()
def cadastra_clube():
    dados = request.get_json()
    clube = Clube(nome_clube=dados['nome'])
    db.session.add(clube)
    db.session.commit()
    return 'Clube Cadastrado'


@app.route('/atualizar_clube', methods=['PUT'])
@jwt_required()
def atualizar_clube():
    dados = request.get_json()
    clube = Clube.query.filter_by(nome_clube=dados['nome_antigo']).first()
    clube.nome_clube = dados['nome_novo']
    db.session.commit()
    return 'Atualizado'


@app.route('/deletar_clube', methods=['DELETE'])
@jwt_required()
def deletar_clube():
    dados = request.get_json()
    clube = Clube.query.filter_by(nome_clube=dados['nome_clube']).first()
    db.session.delete(clube)
    db.session.commit()
    return 'Deletado'


@app.route('/cadastrar_livro', methods=['POST'])
@jwt_required()
def cadastra_livro():
    dados = request.get_json()
    livro = Livro(titulo=dados['titulo'], autor=dados['autor'], clube_id=dados['id_clube'])
    db.session.add(livro)
    db.session.commit()
    return jsonify({'titulo': dados['titulo'], 'autor': dados['autor'], 'id_clube': dados['id_clube']})


@app.route('/listar_livros', methods=['GET'])
@cache.cached(timeout=3600)  # 3600 segundo equivale a 1 hora
def listar_livro():
    livros = Livro.query.all()
    return jsonify([{'titulo': livro.titulo, 'autor': livro.autor} for livro in livros])


@app.route('/registro', methods=['POST'])
@jwt_required()
def registar_avaliacao():
    identidade = pegar_identidade()
    dados = request.get_json()
    usuario = Usuarios.query.filter_by(username=identidade).first()
    avaliacao = Avaliacao(usuario_id=usuario.id, livro_id=dados['id_livro'], nota=dados['nota'],
                          comentario=dados['comentario'])
    db.session.add(avaliacao)
    db.session.commit()
    return jsonify(usuario_id=usuario.id, livro_id=dados['id_livro'], nota=dados['nota'],
                   comentario=dados['comentario'])


@app.route('/estatistica', methods=['GET'])
@cache.cached(timeout=3600)
def media_clube():
    leitura = (Clube.query.join(Livro).join(Avaliacao).all())
    lista = []
    livros_lidos = []
    notas = []
    # Imprimir o dicionário de cada objeto na lista leitura
    for item in leitura:
        lido = []
        nota = []
        for livro in item.livros:
            lista.append(livro.clube_id)
            if item.id == livro.clube_id:
                lido.append(livro.titulo)
            for avalia in livro.avaliacoes:
                if avalia.livro_id == livro.id:
                    nota.append(avalia.nota)
        notas.append(sum(nota) / len(nota))
        livros_lidos.append(lido)
    response = [
        {
            'Livros Lidos': lista.count(item.id),  # Conta quantas vezes o id aparece
            'Clube': item.nome_clube,  # Receber o nome do clube
            'livro': livros_lidos[item.id - 1],  # Acessa o livro pela posição
            'media das notas avaliadas pelo clube': float(f"{notas[item.id - 1]:.2f}")
        }
        for item in leitura  # Itera sobre cada clube de leitura
    ]
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
