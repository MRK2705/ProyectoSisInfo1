import sys
sys.path.append(".")
from flask_mysqldb import MySQL
from flask.wrappers import Request
from flask import Flask, render_template, request, redirect, url_for, flash
from model.recepcionista import Recepcionista
from model.platillo import Platillo
from model.proveedor import Proveedor
from model.producto import Producto
from model.empleado import Empleado

# from tkinter import *
# from tkinter import messagebox as MessageBox
# Clases


app = Flask(__name__, template_folder="../view/templates",
            static_folder="../view/static")
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
        empleado = Empleado(
            request.form['ci'], request.form['nombre'], request.form['fono'], request.form['password'])
        cur = mysql.connection.cursor()
        cur.execute("insert into empleado (ci,nombre,fono,password) values (%s, %s, %s, %s)",
                    (empleado.c, empleado.n, empleado.f, empleado.p))
        mysql.connection.commit()

        return 'recibido'


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST':
        recepcionista = Recepcionista(
            request.form['ci'], request.form['password'])
       # ci = request.form['ci']
       # password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute(
            "select * from empleado where ci=%s and password=%s", (recepcionista.ci, recepcionista.ps))
        dato = cur.fetchall()
        mysql.connection.commit()

        if dato:
            return redirect(url_for("Index"))
        else:
            return render_template('login.html')


@app.route('/to_add_prod')
def to_add_prod():
    cur = mysql.connection.cursor()
    cur.execute("select * from proveedor")
    sqldata = cur.fetchall()

    cur.close()

    arrayProveedores = []
    for e in sqldata:
        print(e)
        proveedor = Proveedor(e[0], e[1], e[2])
        arrayProveedores.append(proveedor)

    print(arrayProveedores)
    return render_template("añadirproducto.html", data=arrayProveedores)


@app.route('/add_prod', methods=['POST'])
def add_prod():
    if request.method == 'POST':
        producto = Producto(0, request.form['nombre'], request.form['cantidad'],
                            request.form['precio_u'], request.form['tipo'], request.form["idproveedor"])

        cur = mysql.connection.cursor()
        cur.execute("insert into producto (nombre,cantidad,precio_u,tipo,proveedor_idproveedor) values (%s, %s, %s,%s,%s)",
                    (producto.n, producto.c, producto.pu, producto.t, producto.idproveedor))
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
        producto = Producto(request.form['idProducto'], request.form['nombre'],
                            request.form['cantidad'], request.form['precio_u'], request.form['tipo'], 0)
        #idProducto = request.form['idProducto']
        #nombre = request.form['nombre']
        #cantidad = request.form['cantidad']
        #precio_u = request.form['precio_u']
        #tipo = request.form['tipo']
        cur = mysql.connection.cursor()
        sq = "UPDATE producto SET nombre=%s,cantidad=%s,precio_u=%s,tipo=%s"
        sq = sq+"WHERE idProducto=%s"
        cur.execute(sq, (producto.n, producto.c, producto.pu,
                         producto.t, producto.idProducto))
        mysql.connection.commit()

        return redirect(url_for('to_productos'))


@app.route("/delete", methods=['POST'])
def delete():
    if(request.method == 'POST'):
        idproducto = (request.form['idProducto'])
        #idProducto = request.form['idProducto']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM producto where idProducto =%s",
                    [idproducto])
        mysql.connection.commit()

        return redirect(url_for('to_productos'))


@app.route('/to_ventas')
def to_ventas():
    cur = mysql.connection.cursor()
    cur.execute("select * from platillo")
    sqldata = cur.fetchall()

    cur.close()

    arrayPlatillos = []
    for e in sqldata:
        print(e)
        if e[1] == True:
            platillo = Platillo(e[0], e[1], e[2], e[3])
            arrayPlatillos.append(platillo)

    print(arrayPlatillos)

    return render_template("ventas.html", data=arrayPlatillos)


@ app.route('/to_registro_ventas')
def to_registro_ventas():
    cur = mysql.connection.cursor()
    cur.execute("select * from compra")
    data = cur.fetchall()
    cur.close()
    return render_template("registroventas.html", compra=data)


@ app.route('/show1')
def show1():
    cur = mysql.connection.cursor()
    cur.execute("select detalle from compra")
    data = cur.fetchall()
    cur.close()
    return render_template("registroventas.html")


@ app.route("/delete1", methods=['POST'])
def delete1():
    if(request.method == 'POST'):
        idCompra = request.form['idCompra']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM compra where idCompra =%s", [idCompra])
        mysql.connection.commit()

        return redirect(url_for('to_registro_ventas'))


@ app.route('/to_platillos')
def to_platillos():
    return render_template("platillos.html")


@ app.route('/to_add_prove')
def to_add_prove():
    return render_template("añadirproveedor.html")


@app.route('/add_prove', methods=['POST'])
def add_prove():
    if request.method == 'POST':
        proveedor = Proveedor(0, request.form['nombre'], request.form['fono'])
        # idProducto = request.form['idProducto']
        #nombre = request.form['nombre']
        #fono = request.form['fono']
        cur = mysql.connection.cursor()
        cur.execute("insert into proveedor (nombre,fono) values (%s, %s)",
                    (proveedor.nombre, proveedor.fono))
        mysql.connection.commit()

        return render_template("index.html")


if __name__ == '__main__':
    app.run(port=3000, debug=True)
