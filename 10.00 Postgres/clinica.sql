
-- =====================================
-- 0. Tabela STATUS
-- =====================================
CREATE TABLE IF NOT EXISTS status (
    status_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 1. Tabela PACIENTES
-- =====================================
CREATE TABLE IF NOT EXISTS pacientes (
    paciente_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo CHAR(1) CHECK (sexo IN ('M', 'F', 'O')),
    telefone VARCHAR(15),
    email VARCHAR(100),
    endereco TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 2. Tabela PROFISSIONAIS
-- =====================================
CREATE TABLE IF NOT EXISTS profissionais (
    profissional_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100),
    registro_profissional VARCHAR(50) UNIQUE NOT NULL,
    data_admissao DATE NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 3. Tabela CONVENIOS
-- =====================================
CREATE TABLE IF NOT EXISTS convenios (
    convenio_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(15),
    email VARCHAR(100),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 4. Tabela AGENDAMENTOS
-- =====================================
CREATE TABLE IF NOT EXISTS agendamentos (
    agendamento_id SERIAL PRIMARY KEY,
    paciente_id INT REFERENCES pacientes(paciente_id) ON DELETE CASCADE,
    profissional_id INT REFERENCES profissionais(profissional_id) ON DELETE CASCADE,
    data_consulta TIMESTAMP NOT NULL,
    status VARCHAR(50) CHECK (status IN ('Marcado', 'Confirmado', 'Cancelado', 'Realizado')),
    convenio_id INT REFERENCES convenios(convenio_id) ON DELETE SET NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 5. Tabela PRONTUARIOS
-- =====================================
CREATE TABLE IF NOT EXISTS prontuarios (
    prontuario_id SERIAL PRIMARY KEY,
    paciente_id INT REFERENCES pacientes(paciente_id) ON DELETE CASCADE,
    profissional_id INT REFERENCES profissionais(profissional_id) ON DELETE CASCADE,
    data_atendimento TIMESTAMP NOT NULL,
    descricao TEXT NOT NULL,
    prescricoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 6. Tabela PAGAMENTOS
-- =====================================
CREATE TABLE IF NOT EXISTS pagamentos (
    pagamento_id SERIAL PRIMARY KEY,
    agendamento_id INT REFERENCES agendamentos(agendamento_id) ON DELETE CASCADE,
    valor NUMERIC(10, 2) NOT NULL,
    data_pagamento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_id INT NOT NULL,  -- Agora referenciamos a tabela STATUS
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Constraint de Foreign Key para a tabela status
    CONSTRAINT fk_pagamentos_status
        FOREIGN KEY (status_id)
        REFERENCES status (status_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- =====================================
-- 7. Tabela MEDICAMENTOS
-- =====================================
CREATE TABLE IF NOT EXISTS medicamentos (
    medicamento_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    estoque INT DEFAULT 0 CHECK (estoque >= 0),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 8. Tabela PRESCRICOES
-- =====================================
CREATE TABLE IF NOT EXISTS prescricoes (
    prescricao_id SERIAL PRIMARY KEY,
    prontuario_id INT REFERENCES prontuarios(prontuario_id) ON DELETE CASCADE,
    medicamento_id INT REFERENCES medicamentos(medicamento_id) ON DELETE CASCADE,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    instrucoes TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);




-- =====================================
-- Populando Tabela PACIENTES
-- =====================================

INSERT INTO pacientes (nome, cpf, data_nascimento, sexo, telefone, email, endereco)
VALUES
('João Silva', '12345678901', '1980-05-15', 'M', '62-99999-1111', 'joao.silva@example.com', 'Rua A, 123'),
('Maria Oliveira', '98765432100', '1990-07-20', 'F', '62-99999-2222', 'maria.oliveira@example.com', 'Rua B, 456'),
('Carlos Pereira', '12312312345', '1985-03-30', 'M', '62-99999-3333', 'carlos.pereira@example.com', 'Rua C, 789'),
('Ana Santos', '23456789012', '1992-02-15', 'F', '62-99999-4444', 'ana.santos@example.com', 'Rua D, 101'),
('Paulo Almeida', '34567890123', '1975-08-10', 'M', '62-99999-5555', 'paulo.almeida@example.com', 'Rua E, 202'),
('Fernanda Costa', '45678901234', '1988-11-25', 'F', '62-99999-6666', 'fernanda.costa@example.com', 'Rua F, 303'),
('Marcos Xavier', '56789012345', '1982-06-30', 'M', '62-99999-7777', 'marcos.xavier@example.com', 'Rua G, 404'),
('Beatriz Nunes', '67890123456', '1995-09-12', 'F', '62-99999-8888', 'beatriz.nunes@example.com', 'Rua H, 505'),
('Ricardo Oliveira', '78901234567', '1983-04-22', 'M', '62-99999-9999', 'ricardo.oliveira@example.com', 'Rua I, 606'),
('Juliana Mendes', '89012345678', '1991-01-18', 'F', '62-99999-1010', 'juliana.mendes@example.com', 'Rua J, 707'),
('Lucas Martins', '90123456789', '1987-03-25', 'M', '62-99999-2020', 'lucas.martins@example.com', 'Rua K, 808'),
('Renata Farias', '01234567890', '1993-07-05', 'F', '62-99999-3030', 'renata.farias@example.com', 'Rua L, 909'),
('Sérgio Rodrigues', '09876543210', '1980-10-30', 'M', '62-99999-4040', 'sergio.rodrigues@example.com', 'Rua M, 100'),
('Clara Lima', '87654321098', '1996-12-15', 'F', '62-99999-5050', 'clara.lima@example.com', 'Rua N, 111'),
('Gabriel Sousa', '76543210987', '1984-09-08', 'M', '62-99999-6060', 'gabriel.sousa@example.com', 'Rua O, 121');

-- =====================================
-- Populando Tabela PROFISSIONAIS
-- =====================================

INSERT INTO profissionais (nome, especialidade, telefone, email, registro_profissional, data_admissao)
VALUES
('Dr. Ana Souza', 'Cardiologia', '62-99999-4444', 'ana.souza@clinica.com', 'CRM12345', '2020-01-10'),
('Dr. Pedro Lima', 'Ortopedia', '62-99999-5555', 'pedro.lima@clinica.com', 'CRM67890', '2021-03-15'),
('Dra. Clara Nunes', 'Dermatologia', '62-99999-6666', 'clara.nunes@clinica.com', 'CRM54321', '2019-07-01'),
('Dr. Ricardo Mendes', 'Pediatria', '62-99999-7777', 'ricardo.mendes@clinica.com', 'CRM98765', '2021-05-20'),
('Dra. Juliana Costa', 'Ginecologia', '62-99999-8888', 'juliana.costa@clinica.com', 'CRM45678', '2018-08-15'),
('Dr. Fernando Silva', 'Neurologia', '62-99999-9999', 'fernando.silva@clinica.com', 'CRM23456', '2017-02-10'),
('Dra. Beatriz Lopes', 'Psiquiatria', '62-99999-1010', 'beatriz.lopes@clinica.com', 'CRM34567', '2022-03-05'),
('Dr. Gustavo Almeida', 'Endocrinologia', '62-99999-2020', 'gustavo.almeida@clinica.com', 'CRM56789', '2020-09-25'),
('Dra. Mariana Ribeiro', 'Oftalmologia', '62-99999-3030', 'mariana.ribeiro@clinica.com', 'CRM67891', '2019-11-11'),
('Dr. Luiz Martins', 'Urologia', '62-99999-4040', 'luiz.martins@clinica.com', 'CRM78912', '2023-01-15');



-- =====================================
-- Populando Tabela CONVENIOS
-- =====================================

INSERT INTO convenios (nome, telefone, email)
VALUES
('Plano Saúde A', '62-88888-1111', 'contato@planoa.com'),
('Plano Saúde B', '62-88888-2222', 'contato@planob.com'),
('Plano Saúde C', '62-88888-3333', 'contato@planoc.com'),
('Viver Bem Saúde', '62-88888-4444', 'contato@viverbem.com'),
('Saúde Total', '62-88888-5555', 'contato@saudetotal.com'),
('Vida Plena', '62-88888-6666', 'contato@vidaplena.com'),
('Protege Saúde', '62-88888-7777', 'contato@protegesaude.com');



-- =====================================
-- Populando Tabela AGENDAMENTOS
-- =====================================

INSERT INTO agendamentos (
    paciente_id, profissional_id, data_consulta, status, convenio_id, descricao
)
VALUES
(1, 1, '2025-05-01 09:00:00', 'Realizado', 1, 'Consulta de rotina cardiológica'),
(2, 2, '2025-05-02 14:30:00', 'Cancelado', 2, 'Dor nas costas persistente'),
(3, 3, '2025-05-03 11:00:00', 'Confirmado', 3, 'Consulta dermatológica'),
(4, 4, '2025-05-04 08:00:00', 'Marcado', 1, 'Acompanhamento pediátrico'),
(5, 5, '2025-05-05 15:00:00', 'Realizado', NULL, 'Check-up ginecológico'),
(6, 6, '2025-05-06 13:00:00', 'Confirmado', 4, 'Consulta neurológica'),
(7, 7, '2025-05-07 10:00:00', 'Marcado', 5, 'Avaliação psiquiátrica inicial'),
(8, 8, '2025-05-08 16:00:00', 'Realizado', 6, 'Controle de diabetes'),
(9, 9, '2025-05-09 09:30:00', 'Cancelado', 7, 'Consulta oftalmológica'),
(10, 10, '2025-05-10 11:30:00', 'Realizado', NULL, 'Exame urológico preventivo');

-- =====================================
-- Populando Tabela PRONTUARIOS
-- =====================================

INSERT INTO prontuarios (
    paciente_id, profissional_id, data_atendimento, descricao, prescricoes
)
VALUES
(1, 1, '2025-05-01 09:00:00', 'Exame de rotina normal. Sinais vitais estáveis.', 'Paracetamol 500mg se necessário.'),
(5, 5, '2025-05-05 15:00:00', 'Exame preventivo ginecológico. Tudo normal.', 'Nenhuma prescrição.'),
(6, 6, '2025-05-06 13:00:00', 'Paciente com queixas de cefaleia recorrente.', 'Dipirona 1g se dor persistir.'),
(8, 8, '2025-05-08 16:00:00', 'Controle de diabetes. Níveis glicêmicos controlados.', 'Manter Metformina 850mg 2x/dia.'),
(10, 10, '2025-05-10 11:30:00', 'Consulta urológica sem alterações relevantes.', 'Atenolol se pressão subir.');


-- =====================================
-- Populando Tabela MEDICAMENTOS
-- =====================================


INSERT INTO medicamentos (nome, descricao, estoque)
VALUES
('Paracetamol', 'Analgésico e antitérmico utilizado no tratamento de dores leves e febre.', 150),
('Amoxicilina', 'Antibiótico de amplo espectro para infecções bacterianas.', 100),
('Ibuprofeno', 'Anti-inflamatório não esteroidal para dores e inflamações.', 120),
('Dipirona', 'Analgesia e redução da febre.', 200),
('Loratadina', 'Antialérgico utilizado para tratar sintomas de alergias.', 80),
('Omeprazol', 'Protetor gástrico usado para tratamento de gastrites e úlceras.', 60),
('Azitromicina', 'Antibiótico usado no tratamento de infecções respiratórias.', 90),
('Metformina', 'Medicamento para controle da diabetes tipo 2.', 130),
('Atenolol', 'Antihipertensivo utilizado no controle da pressão arterial.', 50),
('Melatonina', 'Regulador do sono usado para insônia.', 70),
('Diclofenaco', 'Anti-inflamatório para dores musculares e articulares.', 85),
('Prednisona', 'Corticosteroide usado para tratar inflamações e alergias graves.', 40),
('Fluconazol', 'Antifúngico usado para infecções fúngicas.', 65),
('Clonazepam', 'Ansiolítico e anticonvulsivante usado para transtornos de ansiedade.', 30),
('Captopril', 'Antihipertensivo para controle da pressão arterial.', 95),
('Simeticona', 'Medicamento antiflatulência para redução de gases intestinais.', 150),
('Sildenafil', 'Usado no tratamento de disfunção erétil.', 25),
('Cetoconazol', 'Antifúngico tópico para micoses e dermatites.', 55),
('Salbutamol', 'Broncodilatador para alívio de crises asmáticas.', 70),
('Ranitidina', 'Protetor gástrico para tratamento de úlceras e gastrite.', 80);

-- =====================================
-- Populando Tabela PRESCRICOES
-- =====================================

INSERT INTO prescricoes (prontuario_id, medicamento_id, quantidade, instrucoes)
VALUES
(1, 1, 10, 'Tomar 1 comprimido de 8 em 8 horas em caso de dor.'),             -- Paracetamol
(3, 4, 6, 'Tomar 1 comprimido a cada 6 horas se a dor persistir.'),          -- Dipirona
(4, 8, 60, 'Tomar 1 comprimido de manhã e outro à noite, por 30 dias.'),     -- Metformina
(5, 9, 30, 'Tomar 1 comprimido ao acordar por 30 dias, controle de pressão.'); -- Atenolol



-- =====================================
-- Populando Tabela STATUS
-- =====================================

INSERT INTO status (nome)
VALUES
('Pendente'),   -- status_id = 1
('Pago'),       -- status_id = 2
('Cancelado');  -- status_id = 3



-- =====================================
-- Populando Tabela PAGAMENTOS
-- =====================================

INSERT INTO pagamentos (
    agendamento_id, valor, status_id
)
VALUES
(1, 250.00, 2),
(3, 180.00, 1),
(5, 300.00, 2),
(6, 200.00, 2),
(8, 220.00, 2),
(10, 275.00, 2);
