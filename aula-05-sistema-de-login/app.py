from flask import Flask
from models.database import db
import os
from controllers.routes import init_app

# Criando a instância do Flask com o diretório de templates correto
app = Flask(__name__, template_folder='views')

# Configurações do banco de dados e da aplicação
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'models', 'games.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'chave-secreta-do-app'  # Chave fixa para desenvolvimento

# Inicializando o banco de dados
db.init_app(app)

# Inicializando as rotas
init_app(app)

# Criando as tabelas do banco de dados
with app.app_context():
    try:
        # Garantindo que o diretório models existe
        os.makedirs('models', exist_ok=True)
        
        # Removendo banco antigo se existir
        db_path = os.path.join(basedir, 'models', 'games.sqlite3')
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Banco de dados antigo removido.")
            
        # Criando novo banco e tabelas
        db.create_all()
        print("Banco de dados criado com sucesso em:", db_path)
        
    except Exception as e:
        print("Erro ao criar banco de dados:", str(e))

if __name__ == '__main__':
    app.run(debug=True)
