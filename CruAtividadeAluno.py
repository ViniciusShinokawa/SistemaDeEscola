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

# CREATE - Criar um novo aluno
@app.route('/aluno', methods=['POST'])
def criar_aluno():
    data = request.get_json()
    aluno_id = data['aluno_id']
    nome = data['nome']
    email = data['email']

    query = "INSERT INTO aluno (aluno_id, nome, email) VALUES (%s, %s, %s)"
    values = (aluno_id, nome, email)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"aluno_id": aluno_id}), 201

# READ - Listar todos os alunos
@app.route('/aluno', methods=['GET'])
def listar_alunos():
    cursor.execute("SELECT * FROM aluno")
    results = cursor.fetchall()

    alunos = []
    for row in results:
        alunos.append({
            "aluno_id": row[0],
            "nome": row[1],
            "email": row[2]
        })

    return jsonify(alunos), 200

# READ - Obter um aluno específico
@app.route('/aluno/<aluno_id>', methods=['GET'])
def obter_aluno(aluno_id):
    cursor.execute("SELECT * FROM aluno WHERE aluno_id = %s", (aluno_id,))
    result = cursor.fetchone()

    if result:
        aluno = {
            "aluno_id": result[0],
            "nome": result[1],
            "email": result[2]
        }
        return jsonify(aluno), 200
    else:
        return jsonify({"erro": "Aluno não encontrado"}), 404

# UPDATE - Atualizar os dados de um aluno existente
@app.route('/aluno/<aluno_id>', methods=['PUT'])
def atualizar_aluno(aluno_id):
    data = request.get_json()
    nome = data['nome']
    email = data['email']

    query = "UPDATE aluno SET nome = %s, email = %s WHERE aluno_id = %s"
    values = (nome, email, aluno_id)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"mensagem": "Aluno atualizado com sucesso"}), 200

# DELETE - Excluir um aluno
@app.route('/aluno/<aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    cursor.execute("DELETE FROM aluno WHERE aluno_id = %s", (aluno_id,))
    db.commit()

    return jsonify({"mensagem": "Aluno excluído com sucesso"}), 200

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
