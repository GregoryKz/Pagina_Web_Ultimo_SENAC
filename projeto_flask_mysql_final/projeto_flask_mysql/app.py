from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "chave_super_secreta"

# Conexão com banco MySQL
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="projeto_flask"
    )

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)", (nome, email, senha))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for("login"))
    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        db = conectar()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email=%s AND senha=%s", (email, senha))
        user = cursor.fetchone()
        cursor.close()
        db.close()
        if user:
            session["usuario"] = user["nome"]
            return redirect(url_for("menu"))
        else:
            return render_template("login.html", erro="Email ou senha incorretos")
    return render_template("login.html")

@app.route("/menu")
def menu():
    if "usuario" not in session:
        return redirect(url_for("login"))
    return render_template("menu.html", usuario=session["usuario"])

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/calc", methods=["GET", "POST"])
def calc():
    resultado = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operacao = request.form["operacao"]
            if operacao == "soma":
                resultado = num1 + num2
            elif operacao == "subtracao":
                resultado = num1 - num2
        except ValueError:
            resultado = "Erro: insira apenas números."
    return render_template("calc.html", resultado=resultado)

@app.route("/idade", methods=["GET", "POST"])
def idade():
    mensagem = None
    if request.method == "POST":
        try:
            idade = int(request.form["idade"])
            if idade >= 18:
                mensagem = "Você é maior de idade."
            else:
                mensagem = "Você é menor de idade."
        except ValueError:
            mensagem = "Digite um número válido."
    return render_template("idade.html", mensagem=mensagem)

@app.route("/lista")
def lista():
    numeros = list(range(1, 11))
    return render_template("lista.html", numeros=numeros)

if __name__ == "__main__":
    app.run(debug=True)
