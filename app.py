from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date
from models import db, Atleta, Competicao, Inscricao

app = Flask(__name__)

# ---------------- CONFIGURAÇÃO ----------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- FUNÇÕES AUXILIARES ----------------

def calcular_idade(nascimento):
    hoje = date.today()
    return hoje.year - nascimento.year - (
        (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
    )

# ---------------- DASHBOARD ----------------

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

# ---------------- ATLETAS ----------------

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
        nascimento = datetime.strptime(request.form['nascimento'], '%Y-%m-%d').date()

        atleta = Atleta(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            nascimento=nascimento,
            categoria=request.form['categoria'],
            altura=float(request.form['altura']) if request.form['altura'] else None,
            endereco=request.form['endereco'],
            telefone=request.form['telefone'],
            responsavel=request.form['responsavel'],
            telefone_responsavel=request.form['telefone_responsavel'],
            escola=request.form['escola'],
            local_treino=request.form['local_treino'],
            tamanho_camisa=request.form['tamanho_camisa'],
            numero_camisa=int(request.form['numero_camisa']) if request.form['numero_camisa'] else None,
            padrao_jogo=True if request.form.get('padrao_jogo') == 'sim' else False,
            padrao_treino=True if request.form.get('padrao_treino') == 'sim' else False
        )

        db.session.add(atleta)
        db.session.commit()

        return redirect(url_for('atletas'))

    return render_template('cadastrar_atleta.html')

@app.route('/editar_atleta/<int:id>', methods=['GET', 'POST'])
def editar_atleta(id):
    atleta = Atleta.query.get_or_404(id)

    if request.method == 'POST':
        atleta.nome = request.form['nome']
        atleta.cpf = request.form['cpf']
        atleta.nascimento = datetime.strptime(request.form['nascimento'], '%Y-%m-%d').date()
        atleta.categoria = request.form['categoria']
        atleta.altura = float(request.form['altura']) if request.form['altura'] else None
        atleta.endereco = request.form['endereco']
        atleta.telefone = request.form['telefone']
        atleta.responsavel = request.form['responsavel']
        atleta.telefone_responsavel = request.form['telefone_responsavel']
        atleta.escola = request.form['escola']
        atleta.local_treino = request.form['local_treino']
        atleta.tamanho_camisa = request.form['tamanho_camisa']
        atleta.numero_camisa = int(request.form['numero_camisa']) if request.form['numero_camisa'] else None
        atleta.padrao_jogo = True if request.form.get('padrao_jogo') == 'sim' else False
        atleta.padrao_treino = True if request.form.get('padrao_treino') == 'sim' else False

        db.session.commit()
        return redirect(url_for('atletas'))

    return render_template('editar_atleta.html', atleta=atleta)

@app.route('/remover_atleta/<int:id>')
def remover_atleta(id):
    atleta = Atleta.query.get_or_404(id)
    db.session.delete(atleta)
    db.session.commit()

    return redirect(url_for('atletas'))

# ---------------- COMPETIÇÕES ----------------

@app.route('/competicoes')
def competicoes():
    lista = Competicao.query.all()
    return render_template('competicoes.html', competicoes=lista)

@app.route('/cadastrar_competicao', methods=['GET', 'POST'])
def cadastrar_competicao():
    if request.method == 'POST':
        comp = Competicao(
            nome=request.form['nome'],
            ano=int(request.form['ano']),
            limite=int(request.form['limite'])
        )

        db.session.add(comp)
        db.session.commit()

        return redirect(url_for('competicoes'))

    return render_template('cadastrar_competicao.html')

@app.route('/remover_competicao/<int:id>')
def remover_competicao(id):
    comp = Competicao.query.get_or_404(id)
    db.session.delete(comp)
    db.session.commit()

    return redirect(url_for('competicoes'))

# ---------------- INSCRIÇÕES ----------------

@app.route('/inscrever/<int:competicao_id>', methods=['GET', 'POST'])
def inscrever(competicao_id):
    competicao = Competicao.query.get_or_404(competicao_id)

    if request.method == 'POST':
        atleta_id = int(request.form['atleta_id'])

        total_inscritos = Inscricao.query.filter_by(competicao_id=competicao_id).count()

        if total_inscritos >= competicao.limite:
            return "Limite de atletas atingido!"

        inscricao = Inscricao(
            atleta_id=atleta_id,
            competicao_id=competicao_id
        )

        db.session.add(inscricao)
        db.session.commit()

        return redirect(url_for('competicoes'))

    atletas = Atleta.query.all()
    return render_template('inscrever.html', competicao=competicao, atletas=atletas)
    
    @app.route('/inscricoes')
def inscricoes():
    lista = Inscricao.query.all()
    return render_template('inscricoes.html', inscricoes=lista)

# ---------------- MAIN ----------------

if __name__ == '__main__':
    app.run(debug=True)
    
