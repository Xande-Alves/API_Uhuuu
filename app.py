from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def uhuuu():
    return "<h1>COM O UHUUU!!!, SUA DIVERSÃO É GARANTIDA!</h1>"


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS USERSEACHER(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fotoPerfil TEXT,
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

        conn.execute('''
            CREATE TABLE IF NOT EXISTS EVENTOS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idOfertador INTEGER NOT NULL,
                nome TEXT NOT NULL,
                dataHoraInicio TEXT NOT NULL,
                dataHoraFim TEXT NOT NULL,
                logradouro TEXT NOT NULL,
                numero INTEGER NOT NULL,
                complemento TEXT,
                bairro TEXT NOT NULL,
                cidade TEXT NOT NULL,
                estado TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                descricao TEXT NOT NULL,
                numeroInteresse INTEGER NOT NULL,
                FOREIGN KEY(idOfertador) REFERENCES USEROFFER(id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS FOTOS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            foto TEXT,
            legenda TEXT,
            FOREIGN KEY(evento_id) REFERENCES EVENTOS(id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS ATRACOES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            atracao TEXT,
            atracaoDescricao TEXT,
            FOREIGN KEY(evento_id) REFERENCES EVENTOS(id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS INGRESSOS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            ingresso TEXT,
            ingressoDescricao TEXT,
            FOREIGN KEY(evento_id) REFERENCES EVENTOS(id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS PROMOCOES (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evento_id INTEGER NOT NULL,
            promocao TEXT,
            promocaoDescricao TEXT,
            FOREIGN KEY(evento_id) REFERENCES EVENTOS(id)
            )
        ''')

        conn.execute('''
            CREATE TABLE IF NOT EXISTS MENSAGENS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                idCriador INTEGER NOT NULL,
                foto TEXT,
                nome TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                origem TEXT NOT NULL,
                dataHoraMensagem TEXT NOT NULL,
                FOREIGN KEY(idCriador) REFERENCES USERSEACHER(id)
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
                "fotoPerfil": item[1],
                "nome": item[2],
                "sobrenome": item[3],
                "data_nascimento": item[4],
                "email": item[5],
                "telefone": item[6],
                "senha": item[7]
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


@app.route("/cadastrados_eventos", methods=["GET"])
def listar_eventos():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        eventos = cursor.execute("SELECT * FROM EVENTOS").fetchall()
        eventos_formatados = []

        for item in eventos:
            evento_id = item["id"]

            # Buscar fotos
            fotos = cursor.execute("SELECT foto, legenda FROM FOTOS WHERE evento_id = ?", (evento_id,)).fetchall()
            lista_foto = [{"foto": foto["foto"], "legenda": foto["legenda"]} for foto in fotos]

            # Buscar atrações
            atracoes = cursor.execute("SELECT atracao, atracaoDescricao FROM ATRACOES WHERE evento_id = ?", (evento_id,)).fetchall()
            lista_atracao = [{"atracao": a["atracao"], "atracaoDescricao": a["atracaoDescricao"]} for a in atracoes]

            # Buscar ingressos
            ingressos = cursor.execute("SELECT ingresso, ingressoDescricao FROM INGRESSOS WHERE evento_id = ?", (evento_id,)).fetchall()
            lista_ingresso = [{"ingresso": i["ingresso"], "ingressoDescricao": i["ingressoDescricao"]} for i in ingressos]

            # Buscar promoções
            promocoes = cursor.execute("SELECT promocao, promocaoDescricao FROM PROMOCOES WHERE evento_id = ?", (evento_id,)).fetchall()
            lista_promocao = [{"promocao": p["promocao"], "promocaoDescricao": p["promocaoDescricao"]} for p in promocoes]

            dicionario_eventos = {
                "id": item["id"],
                "idOfertador": item["idOfertador"],
                "nome": item["nome"],
                "dataHoraInicio": item["dataHoraInicio"],
                "dataHoraFim": item["dataHoraFim"],
                "logradouro": item["logradouro"],
                "numero": item["numero"],
                "complemento": item["complemento"],
                "bairro": item["bairro"],
                "cidade": item["cidade"],
                "estado": item["estado"],
                "email": item["email"],
                "telefone": item["telefone"],
                "descricao": item["descricao"],
                "numeroInteresse": item["numeroInteresse"],
                "listaFoto": lista_foto,
                "listaAtracao": lista_atracao,
                "listaIngresso": lista_ingresso,
                "listaPromocao": lista_promocao
            }

            eventos_formatados.append(dicionario_eventos)

    return jsonify(eventos_formatados), 200


@app.route("/mensagens", methods=["GET"])
def listar_mensagens():
    with sqlite3.connect("database.db") as conn:
        conn.row_factory = sqlite3.Row  # permite acessar como dicionário
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MENSAGENS")
        mensagens = [dict(row) for row in cursor.fetchall()]

    return jsonify(mensagens), 200



@app.route("/cadastrar_seacher", methods=["POST"])
def cadastrar_seacher():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido
    fotoPerfil = dados.get("fotoPerfil")
    nome = dados.get("nome")  
    sobrenome = dados.get("sobrenome")  
    data_nascimento = dados.get("data_nascimento")  
    email = dados.get("email")
    telefone = dados.get("telefone")  
    senha = dados.get("senha")  

    if not nome or not sobrenome or not data_nascimento or not email or not telefone or not senha:
        return jsonify({"erro": "Falta preencher campos obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO USERSEACHER (fotoPerfil, nome, sobrenome, data_nascimento, email, telefone, senha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (fotoPerfil, nome, sobrenome, data_nascimento, email, telefone, senha))

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

    if not nome or not logradouro or not numero or not bairro or not cidade or not estado or not email or not telefone or not senha:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO USEROFFER (
            nome, logradouro, numero, complemento, bairro, cidade, estado, email, telefone, senha
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nome, logradouro, numero, complemento, bairro,
            cidade, estado, email, telefone, senha
        ))

    conn.commit()

    return jsonify({"mensagem": "Usuário buscador cadastrado com sucesso."}), 201


@app.route("/cadastrar_evento", methods=["POST"])
def cadastrar_evento():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido
    nome = dados.get("nome")  
    dataHoraInicio = dados.get("dataHoraInicio")
    dataHoraFim = dados.get("dataHoraFim")
    logradouro = dados.get("logradouro")  
    numero = dados.get("numero")  
    complemento = dados.get("complemento")
    bairro = dados.get("bairro")  
    cidade = dados.get("cidade") 
    estado = dados.get("estado")  
    email = dados.get("email")
    telefone = dados.get("telefone")  
    descricao = dados.get("descricao")
    listaFoto = dados.get("listaFoto", [])
    listaAtracao = dados.get("listaAtracao", [])
    listaIngresso = dados.get("listaIngresso", [])
    listaPromocao = dados.get("listaPromocao", [])
    numeroInteresse = dados.get("numeroInteresse")
    idOfertador = dados.get("idOfertador")

    
    if not nome or not logradouro or not numero or not bairro or not cidade or not estado or not email or not telefone or not dataHoraInicio or not dataHoraFim or not descricao or not idOfertador:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO EVENTOS (nome, dataHoraInicio, dataHoraFim, logradouro, numero, complemento, bairro, cidade, estado, email, telefone, descricao, numeroInteresse, idOfertador)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nome, dataHoraInicio, dataHoraFim, logradouro, numero, complemento, bairro,
            cidade, estado, email, telefone, descricao, numeroInteresse, idOfertador
        ))

        evento_id = cursor.lastrowid  # pega o ID do evento recém inserido

        for item in listaFoto:
            foto = item.get("foto")
            legenda = item.get("legenda")
            cursor.execute("""
                INSERT INTO FOTOS (evento_id, foto, legenda)
                VALUES (?, ?, ?)
            """, (evento_id, foto, legenda))

        for item in listaAtracao:
            atracao = item.get("atracao")
            atracaoDescricao = item.get("atracaoDescricao")
            cursor.execute("""
                INSERT INTO ATRACOES (evento_id, atracao, atracaoDescricao)
                VALUES (?, ?, ?)
            """, (evento_id, atracao, atracaoDescricao))

        for item in listaIngresso:
            ingresso = item.get("ingresso")
            ingressoDescricao = item.get("ingressoDescricao")
            cursor.execute("""
                INSERT INTO INGRESSOS (evento_id, ingresso, ingressoDescricao)
                VALUES (?, ?, ?)
            """, (evento_id, ingresso, ingressoDescricao))

        for item in listaPromocao:
            promocao = item.get("promocao")
            promocaoDescricao = item.get("promocaoDescricao")
            cursor.execute("""
                INSERT INTO PROMOCOES (evento_id, promocao, promocaoDescricao)
                VALUES (?, ?, ?)
            """, (evento_id, promocao, promocaoDescricao))


    conn.commit()

    return jsonify({"mensagem": "Evento cadastrado com sucesso."}), 201



@app.route("/cadastrar_mensagem", methods=["POST"])
def cadastrar_mensagem():
    try:
        dados = request.get_json(force=True)
        print("📥 JSON recebido:", dados)

        foto = dados.get("foto")
        nome = dados.get("nome")
        mensagem = dados.get("mensagem")
        origem = dados.get("origem")
        dataHoraMensagem = dados.get("dataHoraMensagem")
        idCriador = dados.get("idCriador")

        campos_faltando = []
        if not nome:
            campos_faltando.append("nome")
        if not mensagem:
            campos_faltando.append("mensagem")
        if not origem:
            campos_faltando.append("origem")
        if not dataHoraMensagem:
            campos_faltando.append("dataHoraMensagem")
        if not idCriador:
            campos_faltando.append("idCriador")

        if campos_faltando:
            return jsonify({
                "erro": f"Campos obrigatórios ausentes: {', '.join(campos_faltando)}"
            }), 400

        if isinstance(idCriador, str) and idCriador.isdigit():
            idCriador = int(idCriador)

        query = """
                INSERT INTO MENSAGENS (idCriador, foto, nome, mensagem, origem, dataHoraMensagem)
                VALUES (?, ?, ?, ?, ?, ?)
                """

        valores = (idCriador, foto, nome, mensagem, origem, dataHoraMensagem)


        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()

        return jsonify({
            "mensagem": "Mensagem cadastrada com sucesso.",
            "dados_recebidos": {
                "foto": foto,
                "nome": nome,
                "mensagem": mensagem,
                "origem": origem,
                "dataHoraMensagem": dataHoraMensagem,
                "idCriador": idCriador,
            }
        }), 201

    except Exception as e:
        print("❌ Erro ao cadastrar mensagem:", str(e))
        return jsonify({"erro": f"Erro interno no servidor: {str(e)}"}), 500



@app.route("/atualizar_seacher", methods=["PUT"])
def atualizar_seacher():
    dados = request.get_json()

    # Extraímos as informações do JSON recebido
    fotoPerfil = dados.get("fotoPerfil")
    nome = dados.get("nome")  
    sobrenome = dados.get("sobrenome")  
    data_nascimento = dados.get("data_nascimento")  
    email = dados.get("email")
    telefone = dados.get("telefone")  
    senha = dados.get("senha")  # pode ser None ou ""

    query_base = """
    UPDATE USERSEACHER SET 
        fotoPerfil = ?,
        nome = ?, 
        sobrenome = ?, 
        data_nascimento = ?, 
        telefone = ?
    """
    params = [fotoPerfil, nome, sobrenome, data_nascimento, telefone]

    if senha:  # Só atualiza se a senha estiver presente e não vazia
        query_base += ", senha = ?"
        params.append(senha)

    query_base += " WHERE email = ?"
    params.append(email)

    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute(query_base, params)
            conn.commit()
        return jsonify({"mensagem": "Usuário buscador alterado com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/atualizar_offer", methods=["PUT"])
def atualizar_offer():
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
    senha = dados.get("senha") # pode ser None ou ""

    query_base = """
    UPDATE USEROFFER SET 
        nome = ?, 
        logradouro = ?, 
        numero = ?, 
        complemento = ?,
        bairro = ?, 
        cidade = ?, 
        estado = ?, 
        telefone = ?
    """
    params = [nome, logradouro, numero, complemento, bairro, cidade, estado, telefone]

    if senha:  # Só atualiza se a senha estiver presente e não vazia
        query_base += ", senha = ?"
        params.append(senha)

    query_base += " WHERE email = ?"
    params.append(email)

    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute(query_base, params)
            conn.commit()
        return jsonify({"mensagem": "Usuário ofertador alterado com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/atualizar_evento", methods=["PUT"])
def atualizar_evento():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido
    id = dados.get("eventoId")
    nome = dados.get("nome")  
    dataHoraInicio = dados.get("dataHoraInicio")
    dataHoraFim = dados.get("dataHoraFim")
    logradouro = dados.get("logradouro")  
    numero = dados.get("numero")  
    complemento = dados.get("complemento")
    bairro = dados.get("bairro")  
    cidade = dados.get("cidade") 
    estado = dados.get("estado")  
    email = dados.get("email")
    telefone = dados.get("telefone")  
    descricao = dados.get("descricao")
    numeroInteresse = dados.get("numeroInteresse", 0)
    listaFoto = dados.get("listaFoto", [])
    listaAtracao = dados.get("listaAtracao", [])
    listaIngresso = dados.get("listaIngresso", [])
    listaPromocao = dados.get("listaPromocao", [])

    query_base = """
    UPDATE EVENTOS SET 
        nome = ?,
        dataHoraInicio = ?,
        dataHoraFim = ?,
        logradouro = ?, 
        numero = ?, 
        complemento = ?,
        bairro = ?, 
        cidade = ?, 
        estado = ?,
        email = ?, 
        telefone = ?,
        descricao = ?,
        numeroInteresse = ?
        WHERE id = ?
    """
    params = [nome, dataHoraInicio, dataHoraFim, logradouro, numero, complemento, bairro, cidade, estado, email, telefone, descricao, numeroInteresse, id]

    try:
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(query_base, params)

            # Fotos
            cursor.execute("DELETE FROM FOTOS WHERE evento_id = ?", (id,))
            for item in listaFoto:
                cursor.execute("INSERT INTO FOTOS (evento_id, foto, legenda) VALUES (?, ?, ?)",
                            (id, item.get("foto"), item.get("legenda")))

            # Atrações
            cursor.execute("DELETE FROM ATRACOES WHERE evento_id = ?", (id,))
            for item in listaAtracao:
                cursor.execute("INSERT INTO ATRACOES (evento_id, atracao, atracaoDescricao) VALUES (?, ?, ?)",
                            (id, item.get("atracao"), item.get("atracaoDescricao")))

            # Ingressos
            cursor.execute("DELETE FROM INGRESSOS WHERE evento_id = ?", (id,))
            for item in listaIngresso:
                cursor.execute("INSERT INTO INGRESSOS (evento_id, ingresso, ingressoDescricao) VALUES (?, ?, ?)",
                            (id, item.get("ingresso"), item.get("ingressoDescricao")))

            # Promoções
            cursor.execute("DELETE FROM PROMOCOES WHERE evento_id = ?", (id,))
            for item in listaPromocao:
                cursor.execute("INSERT INTO PROMOCOES (evento_id, promocao, promocaoDescricao) VALUES (?, ?, ?)",
                            (id, item.get("promocao"), item.get("promocaoDescricao")))

            conn.commit()

        return jsonify({"mensagem": "Evento alterado com sucesso."}), 200
        
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/deletar_seacher", methods=["DELETE"])
def deletar_seacher():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido  
    email = dados.get("email")  

    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute("DELETE FROM USERSEACHER WHERE email = ?", (email,))
            conn.commit()
        return jsonify({"mensagem": "Usuário buscador deletado com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/deletar_offer", methods=["DELETE"])
def deletar_offer():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido  
    email = dados.get("email")  

    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute("DELETE FROM USEROFFER WHERE email = ?", (email,))
            conn.commit()
        return jsonify({"mensagem": "Usuário ofertador deletado com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/deletar_evento", methods=["DELETE"])
def deletar_evento():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido  
    id = dados.get("eventoId")  

    try:
        with sqlite3.connect("database.db") as conn:
            conn.execute("DELETE FROM EVENTOS WHERE id = ?", (id,))
            # Fotos
            conn.execute("DELETE FROM FOTOS WHERE evento_id = ?", (id,))
            # Atrações
            conn.execute("DELETE FROM ATRACOES WHERE evento_id = ?", (id,))
            # Ingressos
            conn.execute("DELETE FROM INGRESSOS WHERE evento_id = ?", (id,))
            # Promoções
            conn.execute("DELETE FROM PROMOCOES WHERE evento_id = ?", (id,))
            conn.commit()
        return jsonify({"mensagem": "Evento excluído com sucesso."}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    

if __name__ == "__main__":
    app.run(debug=True)
