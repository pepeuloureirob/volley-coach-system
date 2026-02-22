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

@app.route('/')
def index():
    return render_template(
        'index.html',
        atletas=Atleta.query.count(),
        competicoes=Competicao.query.count()
    )

@app.route('/atletas')
def atletas():
    lista = Atleta.query.all()

    atletas_processados = []
    for atleta in lista:
        atletas_processados.append({
            "id": atleta.id,
            "nome": atleta.nome,
            "cpf": atleta.cpf,
            "categoria": calcular_categoria(atleta.nascimento),
            "numero_camisa": atleta.numero_camisa
        })

    return render_template('atletas.html', atletas=atletas_processados)

@app.route('/cadastrar_atleta', methods=['GET', 'POST'])
def cadastrar_atleta():
    if request.method == 'POST':
        atleta = Atleta(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            nascimento=datetime.strptime(request.form['nascimento'], '%Y-%m-%d'),

            altura=request.form['altura'],
            endereco=request.form['endereco'],
            telefone=request.form['telefone'],

            responsavel_nome=request.form['responsavel_nome'],
            responsavel_telefone=request.form['responsavel_telefone'],

            escola=request.form['escola'],
            local_treino=request.form['local_treino'],

            tamanho_camisa=request.form['tamanho_camisa'],
            numero_camisa=request.form['numero_camisa'],

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
        atleta.nascimento = datetime.strptime(request.form['nascimento'], '%Y-%m-%d')

        atleta.altura = request.form['altura']
        atleta.endereco = request.form['endereco']
        atleta.telefone = request.form['telefone']

        atleta.responsavel_nome = request.form['responsavel_nome']
        atleta.responsavel_telefone = request.form['responsavel_telefone']

        atleta.escola = request.form['escola']
        atleta.local_treino = request.form['local_treino']

        atleta.tamanho_camisa = request.form['tamanho_camisa']
        atleta.numero_camisa = request.form['numero_camisa']

        atleta.padrao_jogo = True if request.form.get('padrao_jogo') == 'sim' else False
        atleta.padrao_treino = True if request.form.get('padrao_treino') == 'sim' else False

        db.session.commit()
        return redirect(url_for('atletas'))

    return render_template('editar_atleta.html', atleta=atleta)

@app.route('/remover_atleta/<int:id>')
def remover_atleta(id):
    atleta = Atleta.query.get_or_404(id)
    Inscricao.query.filter_by(atleta_id=id).delete()
    db.session.delete(atleta)
    db.session.commit()
    return redirect(url_for('atletas'))

if __name__ == '__main__':
    app.run()
