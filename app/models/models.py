from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuarios(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    nome: str = db.Column(db.String(255), nullable=False)
    username: str = db.Column(db.String(40), unique=True, nullable=False)
    hash_senha: str = db.Column(db.Text, nullable=False)
    usuario_avalicao = db.relationship('Avaliacao', cascade='all', backref='Usuarios')

    def set_senha(self, senha_hash):
        self.hash_senha = self.gerar_hash(senha_hash)

    @staticmethod
    def gerar_hash(senha: str):
        return generate_password_hash(senha)

    @staticmethod
    def checar_senha(senha_hash, senha: str):
        return check_password_hash(senha_hash, senha)


class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    clube_id = db.Column(db.Integer, db.ForeignKey('clube.id'), nullable=False)
    avaliacoes = db.relationship('Avaliacao', cascade='all', backref='Livro')


class Clube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_clube = db.Column(db.String(100), nullable=False)
    livros = db.relationship('Livro', cascade='all', backref='Clube')


class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'), nullable=False)
    nota = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text, nullable=True)

