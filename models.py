from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

inscricoes = db.Table('inscricoes',
    db.Column('atleta_id', db.Integer, db.ForeignKey('atleta.id')),
    db.Column('competicao_id', db.Integer, db.ForeignKey('competicao.id'))
)

class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    altura = db.Column(db.String(20))
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(50))
    responsavel = db.Column(db.String(100))
    telefone_responsavel = db.Column(db.String(50))
    escola = db.Column(db.String(100))
    local_treino = db.Column(db.String(100))
    tamanho_camisa = db.Column(db.String(10))
    padrao_jogo = db.Column(db.String(10))
    padrao_treino = db.Column(db.String(10))
    numero_camisa = db.Column(db.String(10))

class Competicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    limite_atletas = db.Column(db.Integer)
    inscritos = db.relationship('Atleta', secondary=inscricoes, backref='competicoes')
