from flask import Flask, render_template, request, redirect, session,flash


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
jogo4 = Jogo('Metal Gear Solid', 'Ação', 'PS2')
lista_jogos = [jogo1, jogo2, jogo3,jogo4]


app = Flask(__name__)
app.secret_key = 'gsr' # chave de segurkey

@app.route('/')
def index():

    return render_template('lista.html', titulo='Games', Subtitulo='Jogos', jogos=lista_jogos)

@app.route('/novo')
def novo():
    return render_template('novo_jogo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista_jogos.append(jogo)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect('/login')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    nome = request.form['usuario']
    senha = request.form['senha']

    if nome == 'admin' and senha == '123456':
        session['usuario_logado'] = nome
        flash(f'{nome} LOGADO com sucesso!')
        return redirect('/')
    else:
        flash('Erro no login. Tente novamente!')
        return redirect('/login')

# rota de teste
@app.route('/ola')
def ola():
    return '<h1>Olá mundo</h1>'

# trecho da app
app.run(host='0.0.0.0', debug=True)