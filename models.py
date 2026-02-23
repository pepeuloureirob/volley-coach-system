from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ---------------- ATLETA ----------------

class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(20), nullable=False)
    nascimento = db.Column(db.Date, nullable=False)
    categoria = db.Column(db.String(20))

    altura = db.Column(db.Float)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(30))

    responsavel = db.Column(db.String(100))
    telefone_responsavel = db.Column(db.String(30))

    escola = db.Column(db.String(100))
    local_treino = db.Column(db.String(100))

    tamanho_camisa = db.Column(db.String(10))
    numero_camisa = db.Column(db.Integer)

    padrao_jogo = db.Column(db.Boolean)
    padrao_treino = db.Column(db.Boolean)

    def __repr__(self):
        return f"<Atleta {self.nome}>"

# ---------------- COMPETIÇÃO ----------------

class Competicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    limite = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Competicao {self.nome} - {self.ano}>"

# ---------------- INSCRIÇÃO ----------------

class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    atleta_id = db.Column(db.Integer, db.ForeignKey('atleta.id'), nullable=False)
    competicao_id = db.Column(db.Integer, db.ForeignKey('competicao.id'), nullable=False)

    atleta = db.relationship('Atleta', backref='inscricoes')
    competicao = db.relationship('Competicao', backref='inscricoes')

    def __repr__(self):
        return f"<Inscricao Atleta {self.atleta_id} - Competicao {self.competicao_id}>"
        
