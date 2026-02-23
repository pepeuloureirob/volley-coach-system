from flask import Flask, render_template, request, redirect, url_for
from datetime import date, datetime

from models import db, Atleta, Competicao, Inscricao

app = Flask(__name__)

# ---------------- CONFIG ----------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------- HELPERS ----------------

def calcular_idade(nascimento):
    hoje = date.today()
    return hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )

def definir_categoria(idade):
    categorias = [13, 15, 17, 18, 19, 20, 21, 23]
    for cat in categorias:
        if idade <= cat:
            return f"Sub {cat}"
    return "Adulto"

# ---------------- ROUTES ----------------

@app.route('/')
def index():
    total_atletas = Atleta.query.count()
    total_competicoes = Competicao.query.count()
    total_inscricoes = Inscricao.query.count()

    return render_template(
        'index.html',
        total_atletas=total_atletas,
        total_competicoes=total_competicoes,
        total_inscricoes=total_inscricoes
    )

# -------- ATLETAS --------

@app.route('/atletas')
def atletas():
    categoria = request.args.get('categoria')

    if categoria:
        lista = Atleta.query.filter_by(categoria=categoria).all()
    else:
        lista = Atleta.query.all()

    return render_template('atletas.html', atletas=lista)

@app.route('/cadastrar_atleta', methods=['GET', 'POST'])
def cadastrar_atleta():
    if request.method == 'POST':
        nascimento = datetime.strptime(
            request.form['nascimento'],
            '%Y-%m-%d'
        ).date()

        idade = calcular_idade(nascimento)

        atleta = Atleta(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            nascimento=nascimento,
            categoria=definir_categoria(idade),

            altura=float(request.form['altura']),
            endereco=request.form['endereco'],
            telefone=request.form['telefone'],

            responsavel=request.form['responsavel'],
            telefone_responsavel=request.form['telefone_responsavel'],

            escola=request.form['escola'],
            local_treino=request.form['local_treino'],

            tamanho_camisa=request.form['tamanho_camisa'],
            numero_camisa=int(request.form['numero_camisa']),

            padrao_jogo=request.form['padrao_jogo'] == 'sim',
            padrao_treino=request.form['padrao_treino'] == 'sim'
        )

        db.session.add(atleta)
        db.session.commit()

        return redirect(url_for('atletas'))

    return render_template('cadastrar_atleta.html')

@app.route('/editar_atleta/<int:id>', methods=['GET', 'POST'])
def editar_atleta(id):
    atleta = Atleta.query.get_or_404(id)

    if request.method == 'POST':
        nascimento = datetime.strptime(
            request.form['nascimento'],
            '%Y-%m-%d'
        ).date()

        idade = calcular_idade(nascimento)

        atleta.nome = request.form['nome']
        atleta.cpf = request.form['cpf']
        atleta.nascimento = nascimento
        atleta.categoria = definir_categoria(idade)

        atleta.altura = float(request.form['altura'])
        atleta.endereco = request.form['endereco']
        atleta.telefone = request.form['telefone']

        atleta.responsavel = request.form['responsavel']
        atleta.telefone_responsavel = request.form['telefone_responsavel']

        atleta.escola = request.form['escola']
        atleta.local_treino = request.form['local_treino']

        atleta.tamanho_camisa = request.form['tamanho_camisa']
        atleta.numero_camisa = int(request.form['numero_camisa'])

        atleta.padrao_jogo = request.form['padrao_jogo'] == 'sim'
        atleta.padrao_treino = request.form['padrao_treino'] == 'sim'

        db.session.commit()

        return redirect(url_for('atletas'))

    return render_template('editar_atleta.html', atleta=atleta)

@app.route('/remover_atleta/<int:id>')
def remover_atleta(id):
    atleta = Atleta.query.get_or_404(id)

    db.session.delete(atleta)
    db.session.commit()

    return redirect(url_for('atletas'))

# -------- COMPETIÇÕES --------

@app.route('/competicoes')
def competicoes():
    lista = Competicao.query.all()
    return render_template('competicoes.html', competicoes=lista)

@app.route('/cadastrar_competicao', methods=['GET', 'POST'])
def cadastrar_competicao():
    if request.method == 'POST':
        competicao = Competicao(
            nome=request.form['nome'],
            ano=int(request.form['ano']),
            limite=int(request.form['limite'])
        )

        db.session.add(competicao)
        db.session.commit()

        return redirect(url_for('competicoes'))

    return render_template('cadastrar_competicao.html')

# -------- INSCRIÇÕES --------

@app.route('/inscricoes', methods=['GET', 'POST'])
def inscricoes():
    atletas = Atleta.query.all()
    competicoes = Competicao.query.all()
    inscricoes = Inscricao.query.all()

    if request.method == 'POST':
        atleta_id = int(request.form['atleta_id'])
        competicao_id = int(request.form['competicao_id'])

        competicao = Competicao.query.get(competicao_id)

        total_inscritos = Inscricao.query.filter_by(
            competicao_id=competicao_id
        ).count()

        if total_inscritos >= competicao.limite:
            return "❌ Limite de atletas atingido nessa competição."

        nova_inscricao = Inscricao(
            atleta_id=atleta_id,
            competicao_id=competicao_id
        )

        db.session.add(nova_inscricao)
        db.session.commit()

        return redirect(url_for('inscricoes'))

    return render_template(
        'inscricoes.html',
        atletas=atletas,
        competicoes=competicoes,
        inscricoes=inscricoes
    )

# ---------------- INIT DB ----------------

with app.app_context():
    db.create_all()

# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run()
