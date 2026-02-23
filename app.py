from flask import Flask, render_template, request, redirect, url_for
from models import db, Atleta, Competicao, Inscricao
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


def calcular_categoria(data_nascimento):
    hoje = date.today()
    idade = hoje.year - data_nascimento.year
    subs = [13, 15, 17, 18, 19, 20, 21, 23]

    for sub in subs:
        if idade <= sub:
            return f"Sub {sub}"
    return "Adulto"


@app.route('/')
def index():
    atletas = Atleta.query.all()
    competicoes = Competicao.query.all()
    return render_template('index.html', atletas=atletas, competicoes=competicoes)


@app.route('/cadastrar_atleta', methods=['GET', 'POST'])
def cadastrar_atleta():
    if request.method == 'POST':
        nascimento = date.fromisoformat(request.form['data_nascimento'])

        atleta = Atleta(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            data_nascimento=nascimento,
            categoria=calcular_categoria(nascimento),
            altura=request.form['altura'],
            endereco=request.form['endereco'],
            telefone=request.form['telefone'],
            responsavel_nome=request.form['responsavel_nome'],
            responsavel_telefone=request.form['responsavel_telefone'],
            escola=request.form['escola'],
            local_treino=request.form['local_treino'],
            tamanho_camisa=request.form['tamanho_camisa'],
            numero_camisa=request.form['numero_camisa'],
            possui_padrao_jogo=request.form['padrao_jogo'] == 'sim',
            possui_padrao_treino=request.form['padrao_treino'] == 'sim'
        )

        db.session.add(atleta)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('cadastrar_atleta.html')


@app.route('/editar_atleta/<int:id>', methods=['GET', 'POST'])
def editar_atleta(id):
    atleta = Atleta.query.get_or_404(id)

    if request.method == 'POST':
        atleta.nome = request.form['nome']
        atleta.telefone = request.form['telefone']
        atleta.altura = request.form['altura']
        atleta.endereco = request.form['endereco']
        atleta.numero_camisa = request.form['numero_camisa']

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('editar_atleta.html', atleta=atleta)


@app.route('/remover_atleta/<int:id>')
def remover_atleta(id):
    atleta = Atleta.query.get_or_404(id)
    db.session.delete(atleta)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/nova_competicao', methods=['GET', 'POST'])
def nova_competicao():
    if request.method == 'POST':
        comp = Competicao(
            nome=request.form['nome'],
            ano=int(request.form['ano']),
            limite=int(request.form['limite'])
        )
        db.session.add(comp)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('nova_competicao.html')


@app.route('/inscrever/<int:atleta_id>/<int:competicao_id>')
def inscrever(atleta_id, competicao_id):
    competicao = Competicao.query.get_or_404(competicao_id)

    if competicao.inscritos_count() >= competicao.limite:
        return "Limite de atletas atingido."

    inscricao = Inscricao(atleta_id=atleta_id, competicao_id=competicao_id)
    db.session.add(inscricao)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
