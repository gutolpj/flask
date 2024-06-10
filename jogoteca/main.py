from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'gsr'  # chave de segurança
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/jogoteca'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Jogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    console = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

# Atualizando as rotas
@app.route('/')
def index():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima='index'))
    else:
        jogos = Jogo.query.filter_by(deleted_at=None).all()
        return render_template('lista.html', titulo='Games', Subtitulo='Jogos', jogos=jogos)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect(url_for('login', proxima='novo'))
    else:
        return render_template('novo_jogo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    db.session.add(jogo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST',])
def autenticar():
    nome = request.form['usuario']
    senha = request.form['senha']
    proxima = request.form['proxima']

    usuario = Usuario.query.filter_by(nome=nome, senha=senha, deleted_at=None).first()

    if usuario:
        session['usuario_logado'] = nome
        flash(f'{nome} LOGADO com sucesso!')

        if proxima and proxima in app.view_functions:
            return redirect(url_for(proxima))
        else:
            return redirect(url_for('index'))
    else:
        flash('Erro no login. Tente novamente!')
        return redirect(url_for('login'))

@app.route('/usuarios')
def usuarios():
    if 'usuario_logado' not in session or session['usuario_logado'] != 'admin':
        flash('Acesso restrito ao administrador.')
        return redirect(url_for('index'))
    usuarios = Usuario.query.filter_by(deleted_at=None).all()
    return render_template('lista_usuarios.html', usuarios=usuarios, titulo='Usuários')

@app.route('/novo_usuario')
def novo_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] != 'admin':
        flash('Acesso restrito ao administrador.')
        return redirect(url_for('index'))
    return render_template('novo_usuario.html', titulo='Novo Usuário')

@app.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    if 'usuario_logado' not in session or session['usuario_logado'] != 'admin':
        flash('Acesso restrito ao administrador.')
        return redirect(url_for('index'))
    nome = request.form['nome']
    senha = request.form['senha']
    usuario = Usuario(nome, senha)
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('usuarios'))

@app.route('/editar_usuario/<int:id>')
def editar_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] != 'admin':
        flash('Acesso restrito ao administrador.')
        return redirect(url_for('index'))
    usuario = Usuario.query.get(id)
    return render_template('editar_usuario.html', usuario=usuario, titulo='Editar Usuário')

@app.route('/atualizar_usuario/<int:id>', methods=['POST'])
def atualizar_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] != 'admin':
        flash('Acesso restrito ao administrador.')
        return redirect(url_for('index'))
    usuario = Usuario.query.get(id)
    usuario.nome = request.form['nome']
    usuario.senha = request.form['senha']
    db.session.commit()
    return redirect(url_for('usuarios'))

@app.route('/deletar_usuario/<int:id>', methods=['POST'])
def deletar_usuario(id):
    if 'usuario_logado' not in session or session['usuario_logado'] != 'admin':
        flash('Acesso restrito ao administrador.')
        return redirect(url_for('index'))
    usuario = Usuario.query.get(id)
    usuario.deleted_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('usuarios'))

@app.route('/ola')
def ola():
    return '<h1>Olá mundo</h1>'

# Criação do banco de dados e tabelas
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
