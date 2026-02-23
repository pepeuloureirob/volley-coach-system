from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Atleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    cpf = db.Column(db.String(20))
    data_nascimento = db.Column(db.Date)
    categoria = db.Column(db.String(20))

    altura = db.Column(db.String(10))
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))

    responsavel_nome = db.Column(db.String(100))
    responsavel_telefone = db.Column(db.String(20))

    escola = db.Column(db.String(100))
    local_treino = db.Column(db.String(100))

    tamanho_camisa = db.Column(db.String(10))
    numero_camisa = db.Column(db.String(10))

    possui_padrao_jogo = db.Column(db.Boolean)
    possui_padrao_treino = db.Column(db.Boolean)


class Competicao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    ano = db.Column(db.Integer)
    limite = db.Column(db.Integer)

    def inscritos_count(self):
        return Inscricao.query.filter_by(competicao_id=self.id).count()


class Inscricao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atleta_id = db.Column(db.Integer, db.ForeignKey('atleta.id'))
    competicao_id = db.Column(db.Integer, db.ForeignKey('competicao.id'))
