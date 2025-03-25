from flask import render_template, request, redirect, url_for, flash
# Importando o Model
from models.database import db, Game, Usuario
# Essa biblioteca serve para ler uma determinada URL
import urllib
# Converte dados para o formato json
import json
#importando biblioteca para hash de senha
from werkzeug.security import generate_password_hash,check_password_hash

jogadores = []

gamelist = [{'titulo': 'CS-GO',
             'ano': 2012,
             'categoria': 'FPS Online'}]


def init_app(app):
    @app.route('/')
    # View function -> função de visualização
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0]
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))

        return render_template('games.html',
                               game=game,
                               jogadores=jogadores)

    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)
            return (redirect(url_for('cadgames')))
        return render_template('cadgames.html', gamelist=gamelist)

    @app.route('/apigames', methods=['GET', 'POST'])
    # Passando parâmetros para a rota
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    # Definindo que o parâmetro é opcional
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        res = urllib.request.urlopen(url)
        # print(res)
        data = res.read()
        gamesjson = json.loads(data)

        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo = g
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Game com a ID {id} não foi encontrado.'

        return render_template('apigames.html',
                               gamesjson=gamesjson)

    # ROTA COM O CRUD DE JOGOS
    @app.route('/estoque', methods=['GET', 'POST'])
    @app.route('/estoque/delete/<int:id>')
    def estoque(id=None):
        if id:
            # Selecionando o jogo no banco para ser excluído
            game = Game.query.get(id)
            # Deletar o game pea ID
            db.session.delete(game)
            db.session.commit()
            return redirect(url_for('estoque'))
            
        if request.method == 'POST':
            # Cadastra um novo jogo
            newgame = Game(request.form['titulo'], request.form['ano'], request.form['categoria'], request.form['plataforma'], request.form['preco'], request.form['quantidade'])
            # Envia os valores para o banco
            db.session.add(newgame)
            db.session.commit()
            return redirect(url_for('estoque'))
        
        else:
            # PAGINAÇÃO
            # A variável abaixo captura o valor de 'page' que foi passado pelo método GET
            # Define como padrão o valor 1 e o tipo inteiro
            page = request.args.get('page', 1, type=int)
            # Valor padrão de registros por página (definimos 5)
            per_page = 5
            # Faz um SELECT no banco a partir da página informada (page)
            # Filtra os registros de 3 em 3 (per_page)
            games_page = Game.query.paginate(page=page, per_page=per_page)
            return render_template('estoque.html', gamesestoque=games_page)
    
    # ROTA DE EDIÇÃO
    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit(id):
        # Buscando informações do jogo:
        game = Game.query.get(id)
        # Edita o jogo com as informações do formulário
        if request.method == 'POST':
            game.titulo = request.form['titulo']
            game.ano = request.form['ano']
            game.categoria = request.form['categoria']
            game.plataforma = request.form['plataforma']
            game.preco = request.form['preco']
            game.quantidade = request.form['quantidade']
            db.session.commit()
            return redirect(url_for('estoque'))
        return render_template('editgame.html', game=game)

    #rota de login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            user = Usuario.query.filter_by(email=email).first()
            
            if user and check_password_hash(user.password, password):
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Email ou senha inválidos!', 'error')
                return redirect(url_for('login'))
                
        return render_template('login.html')
        
    #rota de cadastro
    @app.route('/cadastrar', methods=['GET', 'POST'])
    def cadastrar():
        if request.method == 'POST':
            try:
                email = request.form['email']
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                
                print(f"Tentativa de cadastro para email: {email}")  # Log para debug
                
                # Verificando se as senhas coincidem
                if password != confirm_password:
                    flash('As senhas não coincidem!', 'error')
                    return redirect(url_for('cadastrar'))
                
                # Verificando se o usuário já existe
                user_exists = Usuario.query.filter_by(email=email).first()
                if user_exists:
                    flash('Email já cadastrado!', 'error')
                    return redirect(url_for('cadastrar'))
                    
                # Gerando o hash
                hashed_password = generate_password_hash(password, method='scrypt')
                new_user = Usuario(email=email, password=hashed_password)
                
                print(f"Novo usuário criado: {new_user}")  # Log para debug
                
                db.session.add(new_user)
                db.session.commit()
                
                print("Usuário salvo com sucesso no banco")  # Log para debug
                
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('login'))
                
            except Exception as e:
                db.session.rollback()
                print(f"Erro ao cadastrar usuário: {str(e)}")  # Log do erro
                flash(f'Erro ao cadastrar. Detalhes: {str(e)}', 'error')
                return redirect(url_for('cadastrar'))
            
        return render_template('cad_user.html')