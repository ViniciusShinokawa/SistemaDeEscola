\c template1;

DROP DATABASE IF EXISTS escola;
CREATE DATABASE escola;

\c escola;

CREATE TABLE alunos (
    aluno_id Primary key character int identity(1,1) NOT NULL,
    nome_completo character varying(40) NOT NULL,
    data_nascimento date NOT NULL,  
    id_turma int FK REFERENCES turma(id_turma),
    nome_responsavel character varying(40) NOT NULL,
    telefone_responsavel character varying(24) NOT NULL,
    email_responsavel character varying(40) NOT NULL,
    informacoes_adicionais text character varying(1000) NOT NULL,
);

CREATE TABLE turma ( 
id_turma Primary key character int identity(1,1) NOT NULL,
professor_id int FK REFERENCES professor(id_professor),
nome_turma character varying(40) NOT NULL,
horario character varying(10) NOT NULL,

);

CREATE TABLE professor (
id_professor Primary key character int identity(1,1) NOT NULL,
nome character varying(40) NOT NULL,
email character varying(40) NOT NULL,
telefone character varying(24) NOT NULL,

);


CREATE TABLE pagamento(
    id_pagamento primary key character int identity(1,1) NOT NULL, 
    aluno_id character INT NOT NULL,
    data_pagamento date NOT NULL,
    valor_pago decimal(10,2),
    forma_pagamento character varying(15),
    referencia character varying(40),
    status_pagamento character varying(15)
);

CREATE TABLE presenca(
    id_presenca primary key character int identity(1,1) NOT NULL,
    aluno_id FK REFERENCES alunos(aluno_id),
    data_presenca date NOT NULL,
    status_presenca BOOLEAN NOT NULL
);

CREATE TABLE atividade (
    id_atividade primary key character int identity(1,1) NOT NULL,
    descricao character varying(40) NOT NULL,
    data_realizacao date NOT NULL,  
)

CREATE TABLE atividade_aluno (
    id_atividade FK REFERENCES atividade(id_atividade),
    aluno_id character varying(5) NOT NULL,
    Primary Key (id_atividade, aluno_id),
    
)

CREATE TABLE usuario (
    id_usuario Primary key character int identity(1,1) NOT NULL,
    login character varying(1000) UNIQUE NOT NULL,
    senha hash character varying(1000) NOT NULL,
    nivel_acesso character varying(15) NOT NULL
    id_professor int FK REFERENCES professor(id_professor),
)

INSERT INTO alunos (aluno_id, nome, endereco, cidade, estado, cep, pais, telefone) VALUES
('A001', 'Lucas Nogueira', 'Av. Flores, 150', 'Campinas', 'SP', '11111-111', 'Brasil', '1010-2020'),
('A002', 'Sofia Martins', 'Rua Azul, 321', 'Niterói', 'RJ', '22222-222', 'Brasil', '2020-3030'),
('A003', 'Gustavo Ferreira', 'Travessa Sol, 456', 'Uberlândia', 'MG', '33333-333', 'Brasil', '3030-4040'),
('A004', 'Letícia Alves', 'Praça Estrelas, 789', 'Caxias do Sul', 'RS', '44444-444', 'Brasil', '4040-5050'),
('A005', 'Eduardo Rocha', 'Beco Jardim, 101', 'Londrina', 'PR', '55555-555', 'Brasil', '5050-6060'),
('A006', 'Camila Barbosa', 'Rua Pôr-do-Sol, 202', 'Aracaju', 'SE', '66666-666', 'Brasil', '6060-7070'),
('A007', 'Rafael Costa', 'Av. Brisa, 303', 'Natal', 'RN', '77777-777', 'Brasil', '7070-8080'),
('A008', 'Carolina Mendes', 'Travessa Luar, 404', 'Belém', 'PA', '88888-888', 'Brasil', '8080-9090'),
('A009', 'Henrique Farias', 'Rua Nuvens, 505', 'João Pessoa', 'PB', '99999-999', 'Brasil', '9090-1010'),
('A010', 'Isabela Teixeira', 'Av. Vento, 606', 'Florianópolis', 'SC', '10101-010', 'Brasil', '1010-2020');
