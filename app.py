from tkinter import *
from tkinter import messagebox as MessageBox
from flask import Flask, render_template, request, redirect, url_for, flash
from flask.wrappers import Request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pizzeria'
mysql = MySQL(app)

@app.route('/inicio')
def Index():
    return render_template('index.html')


@app.route('/to_add_emp')
def to_add_emp():
    return render_template("añadirempleado.html")


@app.route('/add_emp', methods=['POST'])
def add_emp():
    if request.method == 'POST':
        ci = request.form['ci']
        nombre = request.form['nombre']
        fono = request.form['fono']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("insert into empleado (ci,nombre,fono,password) values (%s, %s, %s, %s)",
                    (ci, nombre, fono, password))
        mysql.connection.commit()

        return 'recibido'


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST':
        ci = request.form['ci']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "select * from empleado where ci=%s and password=%s", (ci, password))
        dato = cur.fetchall()
        mysql.connection.commit()

        if dato:
            return redirect(url_for("Index"))
        else:

            MessageBox.showwarning(
                "Alerta!", "Usuario o contraseña incorrectos")

            return render_template('login.html')


@app.route('/to_add_prod')
def to_add_prod():
    return render_template("añadirproducto.html")


@app.route('/add_prod', methods=['POST'])
def add_prod():
    if request.method == 'POST':
        # idProducto = request.form['idProducto']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio_u = request.form['precio_u']
        tipo = request.form['tipo']
        cur = mysql.connection.cursor()
        cur.execute("insert into producto (nombre,cantidad,precio_u,tipo) values (%s, %s, %s,%s)",
                    (nombre, cantidad, precio_u, tipo))
        mysql.connection.commit()

        return render_template("index.html")


@app.route('/to_productos')
def to_productos():
    cur = mysql.connection.cursor()
    cur.execute("select * from producto")
    data = cur.fetchall()
    cur.close()
    return render_template('productos.html', producto=data)


@app.route("/update", methods=['POST'])
def update():
    if(request.method == 'POST'):
        idProducto = request.form['idProducto']
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio_u = request.form['precio_u']
        tipo = request.form['tipo']
        cur = mysql.connection.cursor()
        sq = "UPDATE producto SET nombre=%s,cantidad=%s,precio_u=%s,tipo=%s"
        sq = sq+"WHERE idProducto=%s"
        cur.execute(sq, (nombre, cantidad, precio_u, tipo, idProducto))
        mysql.connection.commit()

        return redirect(url_for('to_productos'))


@app.route("/delete", methods=['POST'])
def delete():
    if(request.method == 'POST'):
        idProducto = request.form['idProducto']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM producto where idProducto =%s", [idProducto])
        mysql.connection.commit()

        return redirect(url_for('to_productos'))


@app.route('/to_ventas')
def to_ventas():
    cur = mysql.connection.cursor()
    cur.execute("select * from platillo")
    sqldata = cur.fetchall()
    print((sqldata))
    cur.close()
    dataPlatillos=[]
    for e in sqldata:
        if e[1] == True:
            dataPlatillos.append({
                "id": e[0],
                "name": e[2],
                "precio": e[3],
                "resumen": f"{e[0]} - {e[2]} - {e[3]} Bs"
            })

    print(dataPlatillos)

    return render_template("ventas.html", data = dataPlatillos)


@ app.route('/to_registro_ventas')
def to_registro_ventas():
    cur=mysql.connection.cursor()
    cur.execute("select * from compra")
    data=cur.fetchall()
    cur.close()
    return render_template("registroventas.html", compra = data)


@ app.route('/show1')
def show1():
    cur=mysql.connection.cursor()
    cur.execute("select detalle from compra")
    data=cur.fetchall()
    cur.close()
    return render_template("registroventas.html")


@ app.route("/delete1", methods = ['POST'])
def delete1():
    if(request.method == 'POST'):
        idCompra=request.form['idCompra']
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM compra where idCompra =%s", [idCompra])
        mysql.connection.commit()

        return redirect(url_for('to_registro_ventas'))


@ app.route('/to_platillos')
def to_platillos():
    return render_template("platillos.html")


if __name__ == '__main__':
    app.run(port = 3000, debug = True)
