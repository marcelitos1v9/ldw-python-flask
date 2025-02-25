from flask import render_template, request, redirect, url_for
import urllib
import json

jogadores = []
gamelist = [{"Titulo": "CS-GO",
         "Ano": 2017,
          "Categoria": "FPS-Online"
         }, {
             
         }]


def init_app(app):
    # criando a primeira rota da aplicação
    @app.route('/')
    # view function -> função de visualização
    def home():
        return render_template('index.html')

    @app.route('/games', methods=['POST', 'GET'])
    def games():
        games = gamelist[0]
        if request.method == 'POST':
            nome_jogador = request.form.get('Jogador')
            jogadores.append(nome_jogador)
            return redirect(url_for('games'))

        return render_template('games.html', games=games, jogadores=jogadores)

    @app.route('/cad_games', methods=['GET', 'POST'])
    def cad_games():
        if request.method == 'POST':
            novo_jogo = {
                "Titulo": request.form.get('titulo'),
                "Ano": int(request.form.get('ano')),
                "Categoria": request.form.get('categoria')
            }
            gamelist.append(novo_jogo)
            return redirect(url_for('cad_games'))
        return render_template('cad_games.html',gamelist=gamelist)
    
    @app.route('/apigames', methods=['GET', 'POST'])
    @app.route('/apigames/<int:id>', methods=['GET', 'POST'])
    def apigames(id=None):
        url = 'https://www.freetogame.com/api/games'
        response = urllib.request.urlopen(url)
        data = response.read()
        gamesjson = json.loads(data)
        if id:
            ginfo = []
            for g in gamesjson:
                if g['id'] == id:
                    ginfo=g 
                    break
            if ginfo:
                return render_template('gameinfo.html', ginfo=ginfo)
            else:
                return f'Jogo com {id} não encontrado'
                    
        return render_template('apigames.html',gamesjson=gamesjson)
