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

# CREATE - Criar uma nova atividade
@app.route('/atividade', methods=['POST'])
def criar_atividade():
    data = request.get_json()
    descricao = data['descricao']
    data_realizacao = data['data_realizacao']

    query = "INSERT INTO atividade (descricao, data_realizacao) VALUES (%s, %s)"
    values = (descricao, data_realizacao)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"id_atividade": cursor.lastrowid}), 201

# READ - Listar todas as atividades
@app.route('/atividade', methods=['GET'])
def listar_atividades():
    cursor.execute("SELECT * FROM atividade")
    results = cursor.fetchall()

    atividades = []
    for row in results:
        atividades.append({
            "id_atividade": row[0],
            "descricao": row[1],
            "data_realizacao": row[2]
        })

    return jsonify(atividades), 200

# READ - Obter uma atividade específica
@app.route('/atividade/<int:id>', methods=['GET'])
def obter_atividade(id):
    cursor.execute("SELECT * FROM atividade WHERE id_atividade = %s", (id,))
    result = cursor.fetchone()

    if result:
        atividade = {
            "id_atividade": result[0],
            "descricao": result[1],
            "data_realizacao": result[2]
        }
        return jsonify(atividade), 200
    else:
        return jsonify({"erro": "Atividade não encontrada"}), 404

# UPDATE - Atualizar uma atividade existente
@app.route('/atividade/<int:id>', methods=['PUT'])
def atualizar_atividade(id):
    data = request.get_json()
    descricao = data['descricao']
    data_realizacao = data['data_realizacao']

    query = "UPDATE atividade SET descricao = %s, data_realizacao = %s WHERE id_atividade = %s"
    values = (descricao, data_realizacao, id)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"mensagem": "Atividade atualizada com sucesso"}), 200

# DELETE - Excluir uma atividade
@app.route('/atividade/<int:id>', methods=['DELETE'])
def excluir_atividade(id):
    cursor.execute("DELETE FROM atividade WHERE id_atividade = %s", (id,))
    db.commit()

    return jsonify({"mensagem": "Atividade excluída com sucesso"}), 200

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
