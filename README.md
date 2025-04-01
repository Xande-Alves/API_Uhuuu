# Api do site do Uhuuu!!!

Esta é uma API feita com Flask e SQLite para o site do Uhuuu que permitirá cadastro de usuários buscadores e ofertadores, no futuro será implementada para cadastro de eventos pelos ofertadores.

## Como rodar o projeto

1. Faça o clone do repositório
```bash
git clone https://github.com/Xande-Alves/API_Uhuuu.git
cd nome-do-projeto
```

2. Crie um ambiente virtual (Obrigatório):
```bash
python -m venv venv
source venv/Scripts/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Inicie o servidor:
```bash
python app.py
```

> A API estará disponível em http://127.0.0.1:5000/

---

## Endpoints

### POST /cadastrar_seacher

O endpoint /cadastrar_seacher é utilizado para cadastrar um novo usuário buscador em nossa API.

**Envio informações (JSON):**
```json
{
    "nome": "Alexandre",  
    "sobrenome": "Alves",  
    "data_nascimento": "1985-04-30",
    "email": "alexandre.upe@gmail.com",
    "telefone": "81988974954",
    "senha": "123456"
}
```

**Resposta (201):**
```json
{
    "mensagem":"Usuário buscador cadastrado com sucesso."
}
```

---

### POST /cadastrar_offer

O endpoint /cadastrar_offer é utilizado para cadastrar um novo usuário ofertadores em nossa API.

**Envio informações (JSON):**
```json
{
    "nome": "Bar do Gera", 
    "logradouro": "Rua diversão", 
    "numero": 200, 
    "complemento": "Praça da folia",
    "bairro": "Jardim Atlântico", 
    "cidade": "Olinda", 
    "estado": "PE",  
    "email": "bardogera@gmail.com",
    "telefone": "81988547365",
    "senha": "654321"
}
```

**Resposta (201):**
```json
{
    "mensagem":"Usuário ofertador cadastrado com sucesso."
}
```

---

### GET /cadastrados_seachers

O endpoint /cadastrados_seachers retorna todos os usuários buscadores cadastrados na API.

**Resposta (200):**
```json
{
    "nome": "Jose Augusto",  
    "sobrenome": "Silva",  
    "data_nascimento": "1965-03-10",
    "email": "jasilva@gmail.com",
    "telefone": "81982750502",
    "senha": "987456"
}
```

---

### GET /cadastrados_offers

O endpoint /cadastrados_offers retorna todos os usuários ofertadores cadastrados na API.

**Resposta (200):**
```json
{
    "nome": "Boate Kiss", 
    "logradouro": "Rua balada", 
    "numero": 400, 
    "complemento": "Alameda noturna",
    "bairro": "Boa Viagem", 
    "cidade": "Recife", 
    "estado": "PE",  
    "email": "boatekiss@gmail.com",
    "telefone": "81983507185",
    "senha": "01010202"
}
```

---

