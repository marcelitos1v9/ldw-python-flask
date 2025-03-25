from flask_sqlalchemy import SQLAlchemy
# Criando uma instância do SQLAlchemy
db = SQLAlchemy()

# Classe responsável por criar a entidade "Games" no banco com seus atributos
class Game(db.Model):
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(150), nullable=False)
    plataforma = db.Column(db.String(150), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    
    # Método construtor da classe
    def __init__(self, titulo, ano, categoria, plataforma, preco, quantidade):
        self.titulo = titulo
        self.ano = ano
        self.categoria = categoria
        self.plataforma = plataforma
        self.preco = preco
        self.quantidade = quantidade
        
    def __repr__(self):
        return f'<Game {self.titulo}>'
        
#classe de usuarios
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)  # Aumentado para comportar o hash
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        
    def __repr__(self):
        return f'<Usuario {self.email}>'