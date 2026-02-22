from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    nascimento = db.Column(db.Date, nullable=False)

    altura = db.Column(db.String(10))
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))

    responsavel_nome = db.Column(db.String(100))
    responsavel_telefone = db.Column(db.String(20))

    escola = db.Column(db.String(100))
    local_treino = db.Column(db.String(100))

    tamanho_camisa = db.Column(db.String(10))
    numero_camisa = db.Column(db.String(10))

    padrao_jogo = db.Column(db.Boolean, default=False)
    padrao_treino = db.Column(db.Boolean, default=False)


class Competicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.String(4), nullable=False)
    limite = db.Column(db.Integer, nullable=False)


class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atleta_id = db.Column(db.Integer, db.ForeignKey('atleta.id'))
    competicao_id = db.Column(db.Integer, db.ForeignKey('competicao.id'))

    atleta = db.relationship('Atleta', backref='inscricoes')
    competicao = db.relationship('Competicao', backref='inscricoes')
