from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import Usuarios, Clube, Livro, Avaliacao
