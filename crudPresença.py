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

# CREATE - Criar uma nova presença
@app.route('/presenca', methods=['POST'])
def criar_presenca():
    data = request.get_json()
    aluno_id = data['aluno_id']
    data_presenca = data['data_presenca']
    status_presenca = data['status_presenca']

    query = """INSERT INTO presenca 
               (aluno_id, data_presenca, status_presenca) 
               VALUES (%s, %s, %s)"""
    values = (aluno_id, data_presenca, status_presenca)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"id_presenca": cursor.lastrowid}), 201

# READ - Listar todas as presenças
@app.route('/presenca', methods=['GET'])
def listar_presencas():
    cursor.execute("SELECT * FROM presenca")
    results = cursor.fetchall()

    presencas = []
    for row in results:
        presencas.append({
            "id_presenca": row[0],
            "aluno_id": row[1],
            "data_presenca": row[2],
            "status_presenca": bool(row[3])
        })

    return jsonify(presencas), 200

# READ - Obter uma presença específica
@app.route('/presenca/<int:id>', methods=['GET'])
def obter_presenca(id):
    cursor.execute("SELECT * FROM presenca WHERE id_presenca = %s", (id,))
    result = cursor.fetchone()

    if result:
        presenca = {
            "id_presenca": result[0],
            "aluno_id": result[1],
            "data_presenca": result[2],
            "status_presenca": bool(result[3])
        }
        return jsonify(presenca), 200
    else:
        return jsonify({"erro": "Presença não encontrada"}), 404

# UPDATE - Atualizar uma presença existente
@app.route('/presenca/<int:id>', methods=['PUT'])
def atualizar_presenca(id):
    data = request.get_json()
    aluno_id = data['aluno_id']
    data_presenca = data['data_presenca']
    status_presenca = data['status_presenca']

    query = """UPDATE presenca 
               SET aluno_id = %s, data_presenca = %s, status_presenca = %s 
               WHERE id_presenca = %s"""
    values = (aluno_id, data_presenca, status_presenca, id)

    cursor.execute(query, values)
    db.commit()

    return jsonify({"mensagem": "Presença atualizada com sucesso"}), 200

# DELETE - Excluir uma presença
@app.route('/presenca/<int:id>', methods=['DELETE'])
def excluir_presenca(id):
    cursor.execute("DELETE FROM presenca WHERE id_presenca = %s", (id,))
    db.commit()

    return jsonify({"mensagem": "Presença excluída com sucesso"}), 200

# Iniciar o servidor
if __name__ == '__main__':
    app.run(debug=True)
