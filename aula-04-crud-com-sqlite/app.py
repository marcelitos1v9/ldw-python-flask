from flask import Flask, render_template
from controllers import routes
from models.database import db
#importando a biblioteca OS (comandos de Sistema operacional)
import os


# criando a instancia do Flask na variável app
app = Flask(__name__, template_folder='views')  # representa o nome do arquivo

# Configuração do banco de dados
dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models', 'games.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db.init_app(app)

# Registro das rotas
routes.init_app(app)

# iniciando o servidor
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
