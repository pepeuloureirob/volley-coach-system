from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    categoria = db.Column(db.String(20), nullable=False)

    altura = db.Column(db.String(10))
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    nome_responsavel = db.Column(db.String(100))
    telefone_responsavel = db.Column(db.String(20))
    escola = db.Column(db.String(100))
    local_treino = db.Column(db.String(100))
    tamanho_camisa = db.Column(db.String(10))
    numero_camisa = db.Column(db.String(10))

    possui_padrao_jogo = db.Column(db.String(5))
    possui_padrao_treino = db.Column(db.String(5))


class Competicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.String(10), nullable=False)
    limite_atletas = db.Column(db.Integer, nullable=False)


class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    atleta_id = db.Column(db.Integer, db.ForeignKey('atleta.id'))
    competicao_id = db.Column(db.Integer, db.ForeignKey('competicao.id'))

    atleta = db.relationship('Atleta', backref='inscricoes')
    competicao = db.relationship('Competicao', backref='inscricoes')
