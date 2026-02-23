from flask import Flask, render_template, request, redirect, url_for
from models import db, Atleta, Competicao, Inscricao
from datetime import date, datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///volei.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

SUBS = [13, 15, 17, 18, 19, 20, 21, 23]

def calcular_categoria(data_nascimento):
    ano_atual = date.today().year
    idade = ano_atual - data_nascimento.year

    for sub in SUBS:
        if idade <= sub:
            return f"Sub-{sub}"
    return "Adulto"

@app.route('/')
def index():
    atletas = Atleta.query.all()
    competicoes = Competicao.query.all()
    return render_template('index.html', atletas=atletas, competicoes=competicoes)

# ---------------- ATLETAS ---------------- #

@app.route('/cadastrar_atleta', methods=['GET', 'POST'])
def cadastrar_atleta():
    competicoes = Competicao.query.all()

    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        nascimento = request.form.get('nascimento')

        if not nome or not cpf or not nascimento:
            return "Erro: campos obrigatórios faltando", 400

        nascimento = datetime.strptime(nascimento, "%Y-%m-%d").date()
        categoria = calcular_categoria(nascimento)

        atleta = Atleta(
            nome=nome,
            cpf=cpf,
            data_nascimento=nascimento,
            categoria=categoria,
            altura=request.form.get('altura'),
            endereco=request.form.get('endereco'),
            telefone=request.form.get('telefone'),
            responsavel_nome=request.form.get('responsavel_nome'),
            responsavel_telefone=request.form.get('responsavel_telefone'),
            escola=request.form.get('escola'),
            local_treino=request.form.get('local_treino'),
            tamanho_camisa=request.form.get('tamanho_camisa'),
            possui_padrao_jogo=True if request.form.get('padrao_jogo') == 'sim' else False,
            possui_padrao_treino=True if request.form.get('padrao_treino') == 'sim' else False,
            numero_camisa=request.form.get('numero_camisa')
        )

        db.session.add(atleta)
        db.session.commit()

        competicao_id = request.form.get('competicao_id')
        if competicao_id:
            competicao = Competicao.query.get(int(competicao_id))

            if competicao and competicao.inscricoes.count() < competicao.limite_atletas:
                inscricao = Inscricao(atleta_id=atleta.id, competicao_id=competicao.id)
                db.session.add(inscricao)
                db.session.commit()

        return redirect(url_for('index'))

    return render_template('cadastrar_atleta.html', competicoes=competicoes)

@app.route('/editar_atleta/<int:id>', methods=['GET', 'POST'])
def editar_atleta(id):
    atleta = Atleta.query.get_or_404(id)

    if request.method == 'POST':
        atleta.nome = request.form.get('nome')
        atleta.telefone = request.form.get('telefone')
        atleta.altura = request.form.get('altura')
        atleta.endereco = request.form.get('endereco')
        atleta.responsavel_nome = request.form.get('responsavel_nome')
        atleta.responsavel_telefone = request.form.get('responsavel_telefone')
        atleta.escola = request.form.get('escola')
        atleta.local_treino = request.form.get('local_treino')
        atleta.tamanho_camisa = request.form.get('tamanho_camisa')
        atleta.numero_camisa = request.form.get('numero_camisa')
        atleta.possui_padrao_jogo = True if request.form.get('padrao_jogo') == 'sim' else False
        atleta.possui_padrao_treino = True if request.form.get('padrao_treino') == 'sim' else False

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editar_atleta.html', atleta=atleta)

@app.route('/remover_atleta/<int:id>')
def remover_atleta(id):
    atleta = Atleta.query.get_or_404(id)
    db.session.delete(atleta)
    db.session.commit()
    return redirect(url_for('index'))

# ---------------- COMPETIÇÕES ---------------- #

@app.route('/nova_competicao', methods=['GET', 'POST'])
def nova_competicao():
    if request.method == 'POST':
        nome = request.form.get('nome')
        ano = request.form.get('ano')
        limite = request.form.get('limite')

        competicao = Competicao(
            nome=nome,
            ano=int(ano),
            limite_atletas=int(limite)
        )

        db.session.add(competicao)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('nova_competicao.html')

@app.route('/remover_competicao/<int:id>')
def remover_competicao(id):
    comp = Competicao.query.get_or_404(id)
    db.session.delete(comp)
    db.session.commit()
    return redirect(url_for('index'))

# ---------------- INSCRIÇÕES ---------------- #

@app.route('/inscrever/<int:atleta_id>/<int:competicao_id>')
def inscrever(atleta_id, competicao_id):
    competicao = Competicao.query.get_or_404(competicao_id)

    if competicao.inscricoes.count() >= competicao.limite_atletas:
        return "Limite de atletas atingido"

    inscricao = Inscricao(atleta_id=atleta_id, competicao_id=competicao_id)
    db.session.add(inscricao)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/inscricoes', methods=['GET', 'POST'])
def inscricoes():
    atletas = Atleta.query.all()
    competicoes = Competicao.query.all()

    if request.method == 'POST':
        atleta_id = request.form.get('atleta_id')
        competicao_id = request.form.get('competicao_id')

        atleta = Atleta.query.get(atleta_id)
        competicao = Competicao.query.get(competicao_id)

        if not atleta or not competicao:
            flash('Erro ao inscrever atleta.')
            return redirect('/inscricoes')

        if len(competicao.inscritos) >= competicao.limite_atletas:
            flash('Limite de atletas atingido!')
            return redirect('/inscricoes')

        if atleta in competicao.inscritos:
            flash('Atleta já inscrito nessa competição.')
            return redirect('/inscricoes')

        competicao.inscritos.append(atleta)
        db.session.commit()

        flash('Atleta inscrito com sucesso!')
        return redirect('/inscricoes')

    return render_template(
        'inscricoes.html',
        atletas=atletas,
        competicoes=competicoes
    )

if __name__ == '__main__':
    app.run(debug=True)
