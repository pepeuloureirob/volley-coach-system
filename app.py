from flask import Flask, render_template, request, redirect
from models import db, Atleta, Competicao, Inscricao

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- HOME / DASHBOARD ---------------- #

@app.route('/')
def index():
    atletas = Atleta.query.all()
    competicoes = Competicao.query.all()
    return render_template(
        'index.html',
        atletas=atletas,
        competicoes=competicoes
    )


# ---------------- ATLETAS ---------------- #

@app.route('/novo_atleta', methods=['POST'])
def novo_atleta():
    atleta = Atleta(
        nome=request.form['nome'],
        cpf=request.form['cpf'],
        data_nascimento=request.form['data_nascimento'],
        categoria=request.form['categoria'],
        altura=request.form.get('altura'),
        endereco=request.form.get('endereco'),
        telefone=request.form.get('telefone'),
        nome_responsavel=request.form.get('nome_responsavel'),
        telefone_responsavel=request.form.get('telefone_responsavel'),
        escola=request.form.get('escola'),
        local_treino=request.form.get('local_treino'),
        tamanho_camisa=request.form.get('tamanho_camisa'),
        numero_camisa=request.form.get('numero_camisa'),
        possui_padrao_jogo=request.form.get('possui_padrao_jogo'),
        possui_padrao_treino=request.form.get('possui_padrao_treino')
    )

    db.session.add(atleta)
    db.session.commit()

    return redirect('/')


@app.route('/excluir_atleta/<int:id>')
def excluir_atleta(id):
    atleta = Atleta.query.get(id)
    db.session.delete(atleta)
    db.session.commit()
    return redirect('/')


# ---------------- COMPETIÇÕES ---------------- #

@app.route('/nova_competicao', methods=['POST'])
def nova_competicao():
    competicao = Competicao(
        nome=request.form['nome'],
        ano=request.form['ano'],
        limite_atletas=request.form['limite_atletas']
    )

    db.session.add(competicao)
    db.session.commit()

    return redirect('/')


@app.route('/excluir_competicao/<int:id>')
def excluir_competicao(id):
    competicao = Competicao.query.get(id)
    db.session.delete(competicao)
    db.session.commit()
    return redirect('/')


# ---------------- INSCRIÇÕES ---------------- #

@app.route('/inscrever/<int:atleta_id>/<int:competicao_id>')
def inscrever(atleta_id, competicao_id):

    existente = Inscricao.query.filter_by(
        atleta_id=atleta_id,
        competicao_id=competicao_id
    ).first()

    if existente:
        return redirect('/')

    competicao = Competicao.query.get(competicao_id)

    total = Inscricao.query.filter_by(
        competicao_id=competicao_id
    ).count()

    if total >= competicao.limite_atletas:
        return redirect('/')

    nova = Inscricao(
        atleta_id=atleta_id,
        competicao_id=competicao_id
    )

    db.session.add(nova)
    db.session.commit()

    return redirect('/')


@app.route('/remover_inscricao/<int:id>')
def remover_inscricao(id):
    inscricao = Inscricao.query.get(id)
    db.session.delete(inscricao)
    db.session.commit()
    return redirect('/')


# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
