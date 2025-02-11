from flask import Flask,render_template

#criando a instancia do flask na variavel do app
app = Flask(__name__,template_folder='views')

#criando a primeira rota da aplicação

@app.route('/')
#view function -> função de visualização
def home():
    return render_template('index.html')

#segunda rota 

@app.route('/games')
def games():
    return render_template('games.html')

#terceira rota
    

#iniciar o servidor

if __name__ == '__main__':
    app.run(host="localhost",port=5000,debug=True)