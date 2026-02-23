from flask import Flask, render_template, request, redirect, flash
from models import db, Atleta, Competicao

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret'

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    total_atletas = Atleta.query.count()
    total_competicoes = Competicao.query.count()
    return render_template('index.html',
                           total_atletas=total_atletas,
                           total_competicoes=total_competicoes)

# ================= ATLETAS =================

@app.route('/atletas')
def atletas():
    lista = Atleta.query.all()
    return render_template('atletas.html', atletas=lista)

@app.route('/novo_atleta', methods=['GET', 'POST'])
def novo_atleta():
    if request.method == 'POST':
        atleta = Atleta(
            nome=request.form['nome'],
            altura=request.form['altura'],
            endereco=request.form['endereco'],
            telefone=request.form['telefone'],
            responsavel=request.form['responsavel'],
            telefone_responsavel=request.form['telefone_responsavel'],
            escola=request.form['escola'],
            local_treino=request.form['local_treino'],
            tamanho_camisa=request.form['tamanho_camisa'],
            padrao_jogo=request.form['padrao_jogo'],
            padrao_treino=request.form['padrao_treino'],
            numero_camisa=request.form['numero_camisa']
        )
        db.session.add(atleta)
        db.session.commit()
        flash('Atleta cadastrado com sucesso!')
        return redirect('/atletas')

    return render_template('novo_atleta.html')

@app.route('/editar_atleta/<int:id>', methods=['GET', 'POST'])
def editar_atleta(id):
    atleta = Atleta.query.get_or_404(id)

    if request.method == 'POST':
        atleta.nome = request.form['nome']
        atleta.altura = request.form['altura']
        atleta.endereco = request.form['endereco']
        atleta.telefone = request.form['telefone']
        atleta.responsavel = request.form['responsavel']
        atleta.telefone_responsavel = request.form['telefone_responsavel']
        atleta.escola = request.form['escola']
        atleta.local_treino = request.form['local_treino']
        atleta.tamanho_camisa = request.form['tamanho_camisa']
        atleta.padrao_jogo = request.form['padrao_jogo']
        atleta.padrao_treino = request.form['padrao_treino']
        atleta.numero_camisa = request.form['numero_camisa']

        db.session.commit()
        flash('Atleta atualizado!')
        return redirect('/atletas')

    return render_template('editar_atleta.html', atleta=atleta)

@app.route('/remover_atleta/<int:id>')
def remover_atleta(id):
    atleta = Atleta.query.get_or_404(id)
    db.session.delete(atleta)
    db.session.commit()
    flash('Atleta removido!')
    return redirect('/atletas')

# ================= COMPETIÇÕES =================

@app.route('/competicoes')
def competicoes():
    lista = Competicao.query.all()
    return render_template('competicoes.html', competicoes=lista)

@app.route('/nova_competicao', methods=['GET', 'POST'])
def nova_competicao():
    if request.method == 'POST':
        comp = Competicao(
            nome=request.form['nome'],
            limite_atletas=int(request.form['limite_atletas'])
        )
        db.session.add(comp)
        db.session.commit()
        flash('Competição criada!')
        return redirect('/competicoes')

    return render_template('nova_competicao.html')

# ================= INSCRIÇÕES =================

@app.route('/inscricoes', methods=['GET', 'POST'])
def inscricoes():
    atletas = Atleta.query.all()
    competicoes = Competicao.query.all()

    if request.method == 'POST':
        atleta_id = request.form['atleta_id']
        competicao_id = request.form['competicao_id']

        atleta = Atleta.query.get(atleta_id)
        competicao = Competicao.query.get(competicao_id)

        if len(competicao.inscritos) >= competicao.limite_atletas:
            flash('Limite atingido!')
            return redirect('/inscricoes')

        if atleta in competicao.inscritos:
            flash('Atleta já inscrito!')
            return redirect('/inscricoes')

        competicao.inscritos.append(atleta)
        db.session.commit()
        flash('Inscrição realizada!')
        return redirect('/inscricoes')

    return render_template('inscricoes.html',
                           atletas=atletas,
                           competicoes=competicoes)

if __name__ == '__main__':
    app.run()
