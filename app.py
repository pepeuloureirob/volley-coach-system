from flask import Flask, render_template, request, redirect, url_for
from models import db, Atleta, Competicao, Inscricao
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

SUB_CATEGORIAS = [13, 15, 17, 18, 19, 20, 21, 23]

def calcular_categoria(nascimento):
    ano_atual = date.today().year
    idade_no_ano = ano_atual - nascimento.year

    for sub in SUB_CATEGORIAS:
        if idade_no_ano <= sub:
            return f"Sub-{sub}"

    return "Adulto"

# HOME
@app.route('/')
def index():
    return render_template(
        'index.html',
        atletas=Atleta.query.count(),
        competicoes=Competicao.query.count()
    )

# ATLETAS
@app.route('/atletas')
def atletas():
    filtro = request.args.get('categoria')
    lista = Atleta.query.all()

    atletas_processados = []
    for atleta in lista:
        categoria = calcular_categoria(atleta.nascimento)
        if not filtro or categoria == filtro:
            atletas_processados.append({
                "id": atleta.id,
                "nome": atleta.nome,
                "cpf": atleta.cpf,
                "categoria": categoria
            })

    categorias = [f"Sub-{s}" for s in SUB_CATEGORIAS] + ["Adulto"]

    return render_template('atletas.html', atletas=atletas_processados, categorias=categorias)

# CADASTRAR ATLETA
@app.route('/cadastrar_atleta', methods=['GET', 'POST'])
def cadastrar_atleta():
    if request.method == 'POST':
        atleta = Atleta(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            nascimento=datetime.strptime(request.form['nascimento'], '%Y-%m-%d')
        )
        db.session.add(atleta)
        db.session.commit()
        return redirect(url_for('atletas'))

    return render_template('cadastrar_atleta.html')

# EDITAR ATLETA
@app.route('/editar_atleta/<int:id>', methods=['GET', 'POST'])
def editar_atleta(id):
    atleta = Atleta.query.get_or_404(id)

    if request.method == 'POST':
        atleta.nome = request.form['nome']
        atleta.cpf = request.form['cpf']
        atleta.nascimento = datetime.strptime(request.form['nascimento'], '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for('atletas'))

    return render_template('editar_atleta.html', atleta=atleta)

# REMOVER ATLETA
@app.route('/remover_atleta/<int:id>')
def remover_atleta(id):
    atleta = Atleta.query.get_or_404(id)
    Inscricao.query.filter_by(atleta_id=id).delete()
    db.session.delete(atleta)
    db.session.commit()
    return redirect(url_for('atletas'))

# COMPETIÇÕES
@app.route('/competicoes', methods=['GET', 'POST'])
def competicoes():
    if request.method == 'POST':
        comp = Competicao(
            nome=request.form['nome'],
            ano=request.form['ano'],
            limite=int(request.form['limite'])
        )
        db.session.add(comp)
        db.session.commit()
        return redirect(url_for('competicoes'))

    return render_template('competicoes.html', competicoes=Competicao.query.all())

# INSCRIÇÕES
@app.route('/inscricoes/<int:competicao_id>', methods=['GET', 'POST'])
def inscricoes(competicao_id):
    competicao = Competicao.query.get_or_404(competicao_id)
    inscritos_count = Inscricao.query.filter_by(competicao_id=competicao_id).count()

    if request.method == 'POST':
        if inscritos_count >= competicao.limite:
            return render_template(
                'inscricoes.html',
                competicao=competicao,
                atletas=Atleta.query.all(),
                inscritos=Inscricao.query.filter_by(competicao_id=competicao_id).all(),
                vagas_restantes=0,
                erro="Limite de atletas atingido 🚫",
                calcular_categoria=calcular_categoria
            )

        atleta_id = request.form['atleta_id']
        existe = Inscricao.query.filter_by(
            atleta_id=atleta_id,
            competicao_id=competicao_id
        ).first()

        if not existe:
            db.session.add(Inscricao(atleta_id=atleta_id, competicao_id=competicao_id))
            db.session.commit()

        return redirect(url_for('inscricoes', competicao_id=competicao_id))

    return render_template(
        'inscricoes.html',
        competicao=competicao,
        atletas=Atleta.query.all(),
        inscritos=Inscricao.query.filter_by(competicao_id=competicao_id).all(),
        vagas_restantes=competicao.limite - inscritos_count,
        calcular_categoria=calcular_categoria
    )

# REMOVER INSCRIÇÃO
@app.route('/remover_inscricao/<int:id>')
def remover_inscricao(id):
    insc = Inscricao.query.get_or_404(id)
    comp_id = insc.competicao_id
    db.session.delete(insc)
    db.session.commit()
    return redirect(url_for('inscricoes', competicao_id=comp_id))

if __name__ == '__main__':
    app.run(debug=True)v
