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

# CREATE - Criar um novo professor
@app.route('/professor', methods=['POST'])
def criar_professor():
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    telefone = data['telefone']

    query = "INSERT INTO professor (nome, email, telefone) VALUES (%s, %s, %s)"
    values = (nome, email, telefone)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"id_professor": cursor.lastrowid}), 201

# READ - Listar todos os professores
@app.route('/professor', methods=['GET'])
def listar_professores():
    cursor.execute("SELECT * FROM professor")
    results = cursor.fetchall()

    professores = []
    for row in results:
        professores.append({
            "id_professor": row[0],
            "nome": row[1],
            "email": row[2],
            "telefone": row[3]
        })

    return jsonify(professores), 200

# READ - Obter um professor específico
@app.route('/professor/<int:id>', methods=['GET'])
def obter_professor(id):
    cursor.execute("SELECT * FROM professor WHERE id_professor = %s", (id,))
    result = cursor.fetchone()

    if result:
        professor = {
            "id_professor": result[0],
            "nome": result[1],
            "email": result[2],
            "telefone": result[3]
        }
        return jsonify(professor), 200
    else:
        return jsonify({"erro": "Professor não encontrado"}), 404

# UPDATE - Atualizar um professor existente
@app.route('/professor/<int:id>', methods=['PUT'])
def atualizar_professor(id):
    data = request.get_json()
    nome = data['nome']
    email = data['email']
    telefone = data['telefone']

    query = "UPDATE professor SET nome = %s, email = %s, telefone = %s WHERE id_professor = %s"
    values = (nome, email, telefone, id)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"mensagem": "Professor atualizado com sucesso"}), 200

# DELETE - Excluir um professor
@app.route('/professor/<int:id>', methods=['DELETE'])
def excluir_professor(id):
    cursor.execute("DELETE FROM professor WHERE id_professor = %s", (id,))
    db.commit()

    return jsonify({"mensagem": "Professor excluído com sucesso"}), 200

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
