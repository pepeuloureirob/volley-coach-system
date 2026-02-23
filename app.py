from flask import Flask, render_template, request, redirect, url_for
from models import db, Atleta, Competicao

app = Flask(__name__)

# ================= CONFIGURAÇÃO =================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ================= DASHBOARD =================
@app.route("/")
def index():
    atletas = Atleta.query.all()
    competicoes = Competicao.query.all()
    return render_template(
        "index.html",
        atletas=atletas,
        competicoes=competicoes
    )

# ================= TELA NOVO ATLETA =================
@app.route("/novo_atleta")
def tela_atleta():
    return render_template("cadastrar_atleta.html")

# ================= SALVAR ATLETA =================
@app.route("/salvar_atleta", methods=["POST"])
def salvar_atleta():
    nome = request.form.get("nome")
    cpf = request.form.get("cpf")
    nascimento = request.form.get("nascimento")
    categoria = request.form.get("categoria")

    altura = request.form.get("altura")
    endereco = request.form.get("endereco")
    telefone = request.form.get("telefone")
    responsavel = request.form.get("responsavel")
    telefone_responsavel = request.form.get("telefone_responsavel")
    escola = request.form.get("escola")
    local_treino = request.form.get("local_treino")
    tamanho_camisa = request.form.get("tamanho_camisa")
    padrao_jogo = request.form.get("padrao_jogo")
    padrao_treino = request.form.get("padrao_treino")
    numero_camisa = request.form.get("numero_camisa")

    atleta = Atleta(
        nome=nome,
        cpf=cpf,
        nascimento=nascimento,
        categoria=categoria,
        altura=altura,
        endereco=endereco,
        telefone=telefone,
        responsavel=responsavel,
        telefone_responsavel=telefone_responsavel,
        escola=escola,
        local_treino=local_treino,
        tamanho_camisa=tamanho_camisa,
        padrao_jogo=padrao_jogo,
        padrao_treino=padrao_treino,
        numero_camisa=numero_camisa
    )

    db.session.add(atleta)
    db.session.commit()

    return redirect(url_for("index"))

# ================= EDITAR ATLETA =================
@app.route("/editar_atleta/<int:atleta_id>")
def editar_atleta(atleta_id):
    atleta = Atleta.query.get_or_404(atleta_id)
    return render_template("editar_atleta.html", atleta=atleta)

# ================= ATUALIZAR ATLETA =================
@app.route("/atualizar_atleta/<int:atleta_id>", methods=["POST"])
def atualizar_atleta(atleta_id):
    atleta = Atleta.query.get_or_404(atleta_id)

    atleta.nome = request.form.get("nome")
    atleta.cpf = request.form.get("cpf")
    atleta.nascimento = request.form.get("nascimento")
    atleta.categoria = request.form.get("categoria")

    atleta.altura = request.form.get("altura")
    atleta.endereco = request.form.get("endereco")
    atleta.telefone = request.form.get("telefone")
    atleta.responsavel = request.form.get("responsavel")
    atleta.telefone_responsavel = request.form.get("telefone_responsavel")
    atleta.escola = request.form.get("escola")
    atleta.local_treino = request.form.get("local_treino")
    atleta.tamanho_camisa = request.form.get("tamanho_camisa")
    atleta.padrao_jogo = request.form.get("padrao_jogo")
    atleta.padrao_treino = request.form.get("padrao_treino")
    atleta.numero_camisa = request.form.get("numero_camisa")

    db.session.commit()

    return redirect(url_for("index"))

# ================= REMOVER ATLETA =================
@app.route("/remover_atleta/<int:atleta_id>")
def remover_atleta(atleta_id):
    atleta = Atleta.query.get_or_404(atleta_id)
    db.session.delete(atleta)
    db.session.commit()
    return redirect(url_for("index"))

# ================= TELA NOVA COMPETIÇÃO =================
@app.route("/nova_competicao")
def tela_competicao():
    return render_template("nova_competicao.html")

# ================= SALVAR COMPETIÇÃO =================
@app.route("/salvar_competicao", methods=["POST"])
def salvar_competicao():
    nome = request.form.get("nome")
    ano = request.form.get("ano")
    limite = request.form.get("limite")

    competicao = Competicao(
        nome=nome,
        ano=ano,
        limite=limite
    )

    db.session.add(competicao)
    db.session.commit()

    return redirect(url_for("index"))

# ================= INSCRIÇÃO =================
@app.route("/inscrever/<int:atleta_id>/<int:competicao_id>")
def inscrever(atleta_id, competicao_id):
    atleta = Atleta.query.get_or_404(atleta_id)
    competicao = Competicao.query.get_or_404(competicao_id)

    if atleta not in competicao.atletas:
        if len(competicao.atletas) < int(competicao.limite):
            competicao.atletas.append(atleta)
            db.session.commit()

    return redirect(url_for("index"))

# ================= RODAR APP =================
if __name__ == "__main__":
    app.run(debug=True)
