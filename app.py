from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def vnw():
    return "<h1>COM O UHUUU!!!, SUA DIVERSÃO É GARANTIDA!</h1>"


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS USERSEACHER(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS USEROFFER(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                logradouro TEXT NOT NULL,
                numero INTEGER NOT NULL,
                complemento TEXT,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                senha TEXT NOT NULL
            )
        ''')


init_db()


@app.route("/cadastrados_seachers", methods=["GET"])
def listar_seachers():
    with sqlite3.connect("database.db") as conn:
        seachers = conn.execute(f"SELECT * FROM USERSEACHER").fetchall()
        seachers_formatados = []

        for item in seachers:
            dicionario_seachers = {
                "id": item[0],
                "nome": item[1],
                "sobrenome": item[2],
                "data_nascimento": item[3],
                "email": item[4],
                "telefone": item[5],
                "senha": item[6]
            }
            seachers_formatados.append(dicionario_seachers)

    return jsonify(seachers_formatados), 200


@app.route("/cadastrados_offers", methods=["GET"])
def listar_offers():
    with sqlite3.connect("database.db") as conn:
        offers = conn.execute(f"SELECT * FROM USEROFFER").fetchall()
        offers_formatados = []

        for item in offers:
            dicionario_offers = {
                "id": item[0],
                "nome": item[1],
                "logradouro": item[2],
                "numero": item[3],
                "complemento": item[4],
                "bairro": item[5],
                "cidade": item[6],
                "estado": item[7],
                "email": item[8],
                "telefone": item[9],
                "senha": item[10]
            }
            offers_formatados.append(dicionario_offers)

    return jsonify(offers_formatados), 200


@app.route("/cadastrar_seacher", methods=["POST"])
def cadastrar_seacher():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido
    nome = dados.get("nome")  
    sobrenome = dados.get("sobrenome")  
    data_nascimento = dados.get("data_nascimento")  
    email = dados.get("email")
    telefone = dados.get("telefone")  
    senha = dados.get("senha")  

    if not nome or not sobrenome or not data_nascimento or not email or not telefone or not senha:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO USERSEACHER (nome,sobrenome,data_nascimento,email,telefone,senha) 
        VALUES ("{nome}", "{sobrenome}", "{data_nascimento}", "{email}", "{telefone}", "{senha}")
        """)

    conn.commit()

    return jsonify({"mensagem": "Usuário buscador cadastrado com sucesso."}), 201


@app.route("/cadastrar_offer", methods=["POST"])
def cadastrar_offer():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido
    nome = dados.get("nome")  
    logradouro = dados.get("logradouro")  
    numero = dados.get("numero")  
    complemento = dados.get("complemento")
    bairro = dados.get("bairro")  
    cidade = dados.get("cidade") 
    estado = dados.get("estado")  
    email = dados.get("email")
    telefone = dados.get("telefone")  
    senha = dados.get("senha") 

    if not nome or not logradouro or not numero or not complemento or not bairro or not cidade or not estado or not email or not telefone or not senha:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO USEROFFER (nome,logradouro,numero,complemento,bairro,cidade,estado,email,telefone,senha) 
        VALUES ("{nome}", "{logradouro}", "{numero}", "{complemento}", "{bairro}", "{cidade}", "{estado}", "{email}", "{telefone}", "{senha}")
        """)

    conn.commit()

    return jsonify({"mensagem": "Usuário buscador cadastrado com sucesso."}), 201


if __name__ == "__main__":
    app.run(debug=True)
