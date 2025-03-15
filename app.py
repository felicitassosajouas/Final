from flask import Flask, jsonify, request
from flask_mysqldb import MySQL 
from dotenv import load_dotenv 
import os 
import mysql.connector 

app = Flask(__name__)

load_dotenv()

# conectar con la base de datos 
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')


mysql = MySQL(app) 
app.secret_key = "mysecretSQL"
#1
@app.route('/', methods=['GET'])
def index():
    try: 
        cur = mysql.connection.cursor()
        cur.execute("SELECT NombreCliente, Ciudad FROM Clientes WHERE Pais = 'Spain'")
        clientes = cur.fetchall()
        cur.close()

        return jsonify(clientes) 
    
    except Exception as e:
        return jsonify({"error": str(e)})
#2
@app.route('/productos/gama/herramientas', methods=['GET'])
def productos_herramientas():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Productos WHERE Gama = 'Herramientas'")
    herramienta = cur.fetchall()
    cur.close()
    return jsonify(herramienta) 


#3
@app.route('/oficinas/agregar', methods=['POST'])
def agregar_oficinas():
    oficina = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Oficinas (CodigoOficina, Ciudad, Pais, Region, CodigoPostal, Telefono, LineaDireccion1, LineaDireccion2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (oficina['CodigoOficina'],oficina['Ciudad'],oficina['Pais'],oficina['Region'],oficina['CodigoPostal'],oficina['Telefono'], oficina['LineaDireccion1'], oficina['LineaDireccion2']))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "País agregado"})

#4
@app.route('/pedidos/estado', methods=['GET'])
def pedidos_pendiente_entregado():
    try: 
        cur = mysql.connection.cursor()
        cur.execute("SELECT CodigoPedido,FechaPedido,FechaEsperada,FechaEntrega FROM Pedidos WHERE Estado = 'Pendiente'")
        Pendiente = cur.fetchall()

        
        cur.execute("SELECT FechaPedido,FechaEsperada,FechaEntrega FROM Pedidos WHERE Estado = 'Entregado'")
        Entregado = cur.fetchall()

        cur.close()
        return jsonify(Pendiente, Entregado) 
    
    except Exception as e:
        return jsonify({"error": str(e)})



if __name__ == "__main__":
    app.run(port=5021, debug=True)
