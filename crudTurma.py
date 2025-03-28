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

# CREATE - Criar uma nova turma
@app.route('/turma', methods=['POST'])
def criar_turma():
    data = request.get_json()
    professor_id = data['professor_id']
    nome_turma = data['nome_turma']
    horario = data['horario']

    query = "INSERT INTO turma (professor_id, nome_turma, horario) VALUES (%s, %s, %s)"
    values = (professor_id, nome_turma, horario)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"id_turma": cursor.lastrowid}), 201

# READ - Listar todas as turmas
@app.route('/turma', methods=['GET'])
def listar_turmas():
    cursor.execute("SELECT * FROM turma")
    results = cursor.fetchall()

    turmas = []
    for row in results:
        turmas.append({
            "id_turma": row[0],
            "professor_id": row[1],
            "nome_turma": row[2],
            "horario": row[3]
        })

    return jsonify(turmas), 200

# READ - Obter uma turma específica
@app.route('/turma/<int:id>', methods=['GET'])
def obter_turma(id):
    cursor.execute("SELECT * FROM turma WHERE id_turma = %s", (id,))
    result = cursor.fetchone()

    if result:
        turma = {
            "id_turma": result[0],
            "professor_id": result[1],
            "nome_turma": result[2],
            "horario": result[3]
        }
        return jsonify(turma), 200
    else:
        return jsonify({"erro": "Turma não encontrada"}), 404

# UPDATE - Atualizar uma turma existente
@app.route('/turma/<int:id>', methods=['PUT'])
def atualizar_turma(id):
    data = request.get_json()
    professor_id = data['professor_id']
    nome_turma = data['nome_turma']
    horario = data['horario']

    query = "UPDATE turma SET professor_id = %s, nome_turma = %s, horario = %s WHERE id_turma = %s"
    values = (professor_id, nome_turma, horario, id)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"mensagem": "Turma atualizada com sucesso"}), 200

# DELETE - Excluir uma turma
@app.route('/turma/<int:id>', methods=['DELETE'])
def excluir_turma(id):
    cursor.execute("DELETE FROM turma WHERE id_turma = %s", (id,))
    db.commit()

    return jsonify({"mensagem": "Turma excluída com sucesso"}), 200

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
