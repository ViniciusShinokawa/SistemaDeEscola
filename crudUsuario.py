from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuração do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="sua_base_de_dados"
)

cursor = db.cursor()

# CREATE - Criar um novo usuário
@app.route('/usuario', methods=['POST'])
def criar_usuario():
    data = request.get_json()
    login = data['login']
    senha = data['senha']  # Armazenar o hash da senha é recomendado
    nivel_acesso = data['nivel_acesso']
    id_professor = data['id_professor']

    query = """INSERT INTO usuario 
               (login, senha, nivel_acesso, id_professor) 
               VALUES (%s, %s, %s, %s)"""
    values = (login, senha, nivel_acesso, id_professor)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"id_usuario": cursor.lastrowid}), 201

# READ - Listar todos os usuários
@app.route('/usuario', methods=['GET'])
def listar_usuarios():
    cursor.execute("SELECT * FROM usuario")
    results = cursor.fetchall()

    usuarios = []
    for row in results:
        usuarios.append({
            "id_usuario": row[0],
            "login": row[1],
            "senha": row[2],  # Em produção, não exponha senhas!
            "nivel_acesso": row[3],
            "id_professor": row[4]
        })

    return jsonify(usuarios), 200

# READ - Obter um usuário específico
@app.route('/usuario/<int:id>', methods=['GET'])
def obter_usuario(id):
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s", (id,))
    result = cursor.fetchone()

    if result:
        usuario = {
            "id_usuario": result[0],
            "login": result[1],
            "senha": result[2],  # Em produção, não exponha senhas!
            "nivel_acesso": result[3],
            "id_professor": result[4]
        }
        return jsonify(usuario), 200
    else:
        return jsonify({"erro": "Usuário não encontrado"}), 404

# UPDATE - Atualizar dados de um usuário existente
@app.route('/usuario/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    data = request.get_json()
    login = data['login']
    senha = data['senha']  # Atualização de senha (hash)
    nivel_acesso = data['nivel_acesso']
    id_professor = data['id_professor']

    query = """UPDATE usuario 
               SET login = %s, senha = %s, nivel_acesso = %s, id_professor = %s 
               WHERE id_usuario = %s"""
    values = (login, senha, nivel_acesso, id_professor, id)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"mensagem": "Usuário atualizado com sucesso"}), 200

# DELETE - Excluir um usuário
@app.route('/usuario/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id,))
    db.commit()

    return jsonify({"mensagem": "Usuário excluído com sucesso"}), 200

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
