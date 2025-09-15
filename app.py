from flask import Flask, render_template

app = Flask(__name__)

# Rutas se mantienen igual
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/acerca')
def acerca_de():
    return render_template('acerca.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True)