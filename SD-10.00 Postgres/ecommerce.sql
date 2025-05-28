-- =====================================
-- 1. Tabela STATUS
-- =====================================
CREATE TABLE IF NOT EXISTS status (
    status_id   SERIAL        PRIMARY KEY,
    nome        VARCHAR(50)   NOT NULL UNIQUE,
    criado_em   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 2. Tabela METODOS_PAGAMENTO
-- =====================================
CREATE TABLE IF NOT EXISTS metodos_pagamento (
    metodo_id   SERIAL        PRIMARY KEY,
    nome        VARCHAR(50)   NOT NULL UNIQUE,
    criado_em   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 3. Tabela CLIENTES
-- =====================================
CREATE TABLE IF NOT EXISTS clientes (
    cliente_id      SERIAL       PRIMARY KEY,
    primeiro_nome   VARCHAR(100) NOT NULL,
    ultimo_nome     VARCHAR(100) NOT NULL,
    email           VARCHAR(150) UNIQUE NOT NULL,
    telefone        VARCHAR(20),
    criado_em       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 4. Tabela CATEGORIAS
-- =====================================
CREATE TABLE IF NOT EXISTS categorias (
    categoria_id  SERIAL       PRIMARY KEY,
    nome          VARCHAR(100) NOT NULL,
    descricao     TEXT,
    criado_em     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- =====================================
-- 5. Tabela PRODUTOS
-- =====================================
CREATE TABLE IF NOT EXISTS produtos (
    produto_id      SERIAL         PRIMARY KEY,
    categoria_id    INT            NOT NULL,
    nome            VARCHAR(150)   NOT NULL,
    descricao       TEXT,
    preco           NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    qtd_estoque     INT            NOT NULL DEFAULT 0,
    criado_em       TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Constraint de chave estrangeira (ligação com categorias)
    CONSTRAINT fk_produtos_categoria
        FOREIGN KEY (categoria_id)
        REFERENCES categorias (categoria_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- =====================================
-- 6. Tabela PEDIDOS
-- =====================================
CREATE TABLE IF NOT EXISTS pedidos (
    pedido_id     SERIAL         PRIMARY KEY,
    cliente_id    INT            NOT NULL,
    data_pedido   TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status_id     INT            NOT NULL, -- Referencia a tabela STATUS
    criado_em     TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Constraint de chave estrangeira (ligação com clientes)
    CONSTRAINT fk_pedidos_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES clientes (cliente_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    -- Constraint de chave estrangeira (ligação com status)
    CONSTRAINT fk_pedidos_status
        FOREIGN KEY (status_id)
        REFERENCES status (status_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- =====================================
-- 7. Tabela ITENS_DO_PEDIDO
-- =====================================
CREATE TABLE IF NOT EXISTS itens_do_pedido (
    item_pedido_id   SERIAL          PRIMARY KEY,
    pedido_id        INT             NOT NULL,
    produto_id       INT             NOT NULL,
    quantidade       INT             NOT NULL DEFAULT 1,
    criado_em        TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Constraint de chave estrangeira (ligação com pedidos)
    CONSTRAINT fk_itens_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedidos (pedido_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    -- Constraint de chave estrangeira (ligação com produtos)
    CONSTRAINT fk_itens_produto
        FOREIGN KEY (produto_id)
        REFERENCES produtos (produto_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- =====================================
-- 8. Tabela PAGAMENTOS
-- =====================================
CREATE TABLE IF NOT EXISTS pagamentos (
    pagamento_id     SERIAL         PRIMARY KEY,
    pedido_id        INT            NOT NULL,
    metodo_id        INT            NOT NULL, -- Referencia a tabela METODOS_PAGAMENTO
    data_pagamento   TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    valor            NUMERIC(10, 2) NOT NULL,
    status_id        INT            NOT NULL, -- Referencia a tabela STATUS
    criado_em        TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Constraint de chave estrangeira (ligação com pedidos)
    CONSTRAINT fk_pagamentos_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedidos (pedido_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    -- Constraint de chave estrangeira (ligação com métodos de pagamento)
    CONSTRAINT fk_pagamentos_metodo
        FOREIGN KEY (metodo_id)
        REFERENCES metodos_pagamento (metodo_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    -- Constraint de chave estrangeira (ligação com status)
    CONSTRAINT fk_pagamentos_status
        FOREIGN KEY (status_id)
        REFERENCES status (status_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- ============================
-- Tabela TRANSPORTADORAS
-- ============================
CREATE TABLE IF NOT EXISTS transportadoras (
    transportadora_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- =====================================
-- 9. Tabela REMESSAS (Atualizada)
-- =====================================
CREATE TABLE IF NOT EXISTS remessas (
    remessa_id          SERIAL       PRIMARY KEY,
    pedido_id           INT          NOT NULL,
    transportadora_id   INT          NOT NULL, -- Referencia a tabela TRANSPORTADORAS
    codigo_rastreamento VARCHAR(100),
    data_envio          TIMESTAMP,
    data_entrega        TIMESTAMP,
    status_id           INT          NOT NULL, -- Referencia a tabela STATUS
    criado_em           TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Constraint de chave estrangeira (ligação com pedidos)
    CONSTRAINT fk_remessas_pedido
        FOREIGN KEY (pedido_id)
        REFERENCES pedidos (pedido_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    -- Constraint de chave estrangeira (ligação com transportadoras)
    CONSTRAINT fk_remessas_transportadora
        FOREIGN KEY (transportadora_id)
        REFERENCES transportadoras (transportadora_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    -- Constraint de chave estrangeira (ligação com status)
    CONSTRAINT fk_remessas_status
        FOREIGN KEY (status_id)
        REFERENCES status (status_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);




-- =============================
-- Correção dos valores de Status
-- =============================
INSERT INTO status (status_id, nome, criado_em)
VALUES
(1, 'pendente', '2024-12-29 22:18:20.908803'),
(2, 'concluido', '2024-12-29 22:18:20.908803'),
(3, 'cancelado', '2024-12-29 22:18:20.908803'),
(4, 'pago', '2024-12-29 22:18:20.908803'),
(5, 'falhou', '2024-12-29 22:18:20.908803'),
(6, 'enviado', '2024-12-29 22:18:20.908803'),
(7, 'entregue', '2024-12-29 22:18:20.908803');


-- =====================================
-- INSERTS NA TABELA METODOS_PAGAMENTO
-- =====================================
INSERT INTO metodos_pagamento (nome, criado_em)
VALUES
('cartao_credito', CURRENT_TIMESTAMP),
('boleto', CURRENT_TIMESTAMP),
('pix', CURRENT_TIMESTAMP),
('transferencia_bancaria', CURRENT_TIMESTAMP),
('dinheiro', CURRENT_TIMESTAMP)
ON CONFLICT (nome) DO NOTHING;


-- =====================================
-- INSERTS NA TABELA CLIENTES
-- =====================================
INSERT INTO clientes (cliente_id, primeiro_nome, ultimo_nome, email, telefone, criado_em)
VALUES
(1, 'João', 'Silva', 'joao.silva@example.com', '62-99999-1111', '2024-01-15 09:00:00'),
(2, 'Maria', 'Souza', 'maria.souza@example.com', '62-99999-2222', '2024-02-20 14:30:00'),
(3, 'Carlos', 'Pereira', 'carlos.pereira@example.com', '62-99999-3333', '2024-03-10 18:45:00'),
(4, 'Ana', 'Oliveira', 'ana.oliveira@example.com', '62-99999-4444', '2024-04-25 11:15:00'),
(5, 'Beatriz', 'Fernandes', 'beatriz.fernandes@example.com', '62-99999-5555', '2024-05-12 08:00:00'),
(6, 'Paulo', 'Almeida', 'paulo.almeida@example.com', '62-99999-6666', '2024-06-07 16:20:00'),
(7, 'Fernanda', 'Ribeiro', 'fernanda.ribeiro@example.com', '62-99999-7777', '2024-07-19 13:00:00'),
(8, 'Sérgio', 'Costa', 'sergio.costa@example.com', '62-99999-8888', '2024-08-15 09:45:00'),
(9, 'Mariana', 'Gomes', 'mariana.gomes@example.com', '62-99999-9999', '2024-09-10 17:30:00'),
(10, 'Lucas', 'Batista', 'lucas.batista@example.com', '62-99999-1010', '2024-10-21 12:10:00'),
(11, 'Juliana', 'Farias', 'juliana.farias@example.com', '62-99999-2020', '2024-11-05 10:50:00'),
(12, 'Ricardo', 'Moraes', 'ricardo.moraes@example.com', '62-99999-3030', '2024-11-25 15:20:00'),
(13, 'Marcos', 'Araujo', 'marcos.araujo@example.com', '62-99999-4040', '2024-12-08 18:40:00'),
(14, 'Luana', 'Xavier', 'luana.xavier@example.com', '62-99999-5050', '2024-12-15 07:55:00'),
(15, 'Renata', 'Souza', 'renata.souza@example.com', '62-99999-6060', '2024-12-30 20:15:00');


-- =====================================
-- INSERTS NA TABELA CATEGORIAS
-- =====================================
INSERT INTO categorias (categoria_id, nome, descricao, criado_em)
VALUES
(1, 'Eletrônicos', 'Produtos tecnológicos e gadgets', '2024-01-01 09:00:00'),
(2, 'Livros', 'Livros impressos e digitais', '2024-01-05 10:00:00'),
(3, 'Esportes', 'Artigos esportivos e acessórios', '2024-01-10 11:00:00'),
(4, 'Vestuário', 'Roupas e acessórios de moda', '2024-01-15 12:00:00'),
(5, 'Casa & Cozinha', 'Utensílios domésticos e de cozinha', '2024-01-20 13:00:00'),
(6, 'Jogos & Consoles', 'Consoles, jogos e acessórios', '2024-01-25 14:00:00'),
(7, 'Informática', 'Notebooks, desktops e acessórios', '2024-01-30 15:00:00'),
(8, 'Beleza & Saúde', 'Produtos de cuidados pessoais e beleza', '2024-02-01 16:00:00');



-- =====================================
-- INSERTS NA TABELA PRODUTOS
-- =====================================
INSERT INTO produtos (produto_id, categoria_id, nome, descricao, preco, qtd_estoque, criado_em)
VALUES
(1, 1, 'Smartphone ProMax', 'Celular avançado com câmeras incríveis', 3499.90, 50, '2024-02-10 09:00:00'),
(2, 1, 'Fone Bluetooth SoundX', 'Fone de ouvido com cancelamento de ruído ativo', 299.90, 200, '2024-02-15 10:30:00'),
(3, 2, 'Livro "Aprenda Python"', 'Guia completo para iniciantes em programação', 75.00, 100, '2024-03-01 14:20:00'),
(4, 2, 'Romance Histórico', 'Uma história épica ambientada na Idade Média', 50.00, 80, '2024-03-10 16:45:00'),
(5, 3, 'Bola de Futebol Pro', 'Bola oficial para jogos profissionais', 129.90, 60, '2024-04-05 12:10:00'),
(6, 3, 'Tênis Esportivo Ultra', 'Tênis leve para corrida e atividades físicas', 259.90, 40, '2024-04-20 09:50:00'),
(7, 4, 'Camiseta DryFit', 'Camiseta unissex com tecnologia de secagem rápida', 49.90, 120, '2024-05-01 08:30:00'),
(8, 4, 'Jaqueta Impermeável', 'Jaqueta resistente à água para aventuras', 399.90, 30, '2024-05-15 11:00:00'),
(9, 5, 'Conjunto de Panelas', 'Conjunto antiaderente com 5 peças', 299.90, 50, '2024-06-10 15:20:00'),
(10, 5, 'Cafeteira Automática', 'Cafeteira elétrica com timer programável', 499.90, 25, '2024-06-20 09:00:00'),
(11, 6, 'Console GameStation', 'Console de videogame com gráficos incríveis', 1999.90, 15, '2024-07-05 16:00:00'),
(12, 6, 'Controle Sem Fio Elite', 'Controle de videogame ergonômico com vibração', 249.90, 80, '2024-07-20 10:50:00'),
(13, 7, 'Notebook UltraFast', 'Notebook com processador i7 e SSD de 512GB', 4599.90, 10, '2024-08-01 14:45:00'),
(14, 7, 'Teclado Gamer RGB', 'Teclado mecânico com iluminação personalizável', 299.90, 60, '2024-08-10 18:20:00'),
(15, 8, 'Creme Hidratante', 'Hidratação intensa para todos os tipos de pele', 49.90, 100, '2024-08-20 08:40:00');

-- =====================================
-- INSERTS NA TABELA PEDIDOS
-- =====================================
INSERT INTO pedidos (pedido_id, cliente_id, data_pedido, status_id)
VALUES
(1, 1, '2024-01-05 10:00:00', 1), -- Pendente
(2, 2, '2024-01-07 14:30:00', 2), -- Concluído
(3, 3, '2024-01-08 09:45:00', 3), -- Cancelado
(4, 4, '2024-01-10 11:15:00', 1), -- Pendente
(5, 5, '2024-01-12 17:00:00', 2), -- Concluído
(6, 6, '2024-01-15 08:30:00', 1), -- Pendente
(7, 7, '2024-01-18 12:00:00', 3), -- Cancelado
(8, 8, '2024-01-20 14:50:00', 2), -- Concluído
(9, 9, '2024-01-22 09:30:00', 1), -- Pendente
(10, 10, '2024-01-25 16:40:00', 2), -- Concluído
(11, 11, '2024-01-28 10:20:00', 1), -- Pendente
(12, 12, '2024-01-30 13:10:00', 3), -- Cancelado
(13, 13, '2024-02-02 11:45:00', 1), -- Pendente
(14, 14, '2024-02-05 15:30:00', 2), -- Concluído
(15, 15, '2024-02-08 09:10:00', 1), -- Pendente
(16, 1, '2024-02-10 14:00:00', 3), -- Cancelado
(17, 2, '2024-02-12 11:20:00', 2), -- Concluído
(18, 3, '2024-02-14 16:50:00', 1), -- Pendente
(19, 4, '2024-02-17 10:30:00', 2), -- Concluído
(20, 5, '2024-02-20 13:40:00', 1), -- Pendente
(21, 6, '2024-02-22 15:20:00', 3), -- Cancelado
(22, 7, '2024-02-25 09:30:00', 2), -- Concluído
(23, 8, '2024-02-27 14:15:00', 1), -- Pendente
(24, 9, '2024-03-01 11:40:00', 2), -- Concluído
(25, 10, '2024-03-03 10:10:00', 3), -- Cancelado
(26, 11, '2024-03-05 12:50:00', 1), -- Pendente
(27, 12, '2024-03-07 09:25:00', 2), -- Concluído
(28, 13, '2024-03-09 15:00:00', 1), -- Pendente
(29, 14, '2024-03-11 13:30:00', 3), -- Cancelado
(30, 15, '2024-03-14 14:45:00', 2); -- Concluído


-- ============================
-- Populando ITENS_DO_PEDIDO
-- ============================
INSERT INTO itens_do_pedido (item_pedido_id, pedido_id, produto_id, quantidade, criado_em)
VALUES
-- Pedido 1
(1, 1, 1, 2, CURRENT_TIMESTAMP),
(2, 1, 3, 1, CURRENT_TIMESTAMP),

-- Pedido 2
(3, 2, 5, 1, CURRENT_TIMESTAMP),

-- Pedido 3
(4, 3, 7, 3, CURRENT_TIMESTAMP),
(5, 3, 9, 2, CURRENT_TIMESTAMP),

-- Pedido 4
(6, 4, 10, 1, CURRENT_TIMESTAMP),

-- Pedido 5
(7, 5, 2, 2, CURRENT_TIMESTAMP),
(8, 5, 8, 1, CURRENT_TIMESTAMP),

-- Pedido 6
(9, 6, 11, 1, CURRENT_TIMESTAMP),
(10, 6, 4, 2, CURRENT_TIMESTAMP),

-- Pedido 7
(11, 7, 1, 1, CURRENT_TIMESTAMP),
(12, 7, 14, 1, CURRENT_TIMESTAMP),

-- Pedido 8
(13, 8, 3, 2, CURRENT_TIMESTAMP),

-- Pedido 9
(14, 9, 12, 3, CURRENT_TIMESTAMP),
(15, 9, 6, 1, CURRENT_TIMESTAMP),

-- Pedido 10
(16, 10, 2, 1, CURRENT_TIMESTAMP),
(17, 10, 13, 1, CURRENT_TIMESTAMP),
(18, 10, 7, 2, CURRENT_TIMESTAMP),

-- Pedido 11
(19, 11, 9, 4, CURRENT_TIMESTAMP),

-- Pedido 12
(20, 12, 4, 1, CURRENT_TIMESTAMP),
(21, 12, 11, 3, CURRENT_TIMESTAMP),

-- Pedido 13
(22, 13, 10, 2, CURRENT_TIMESTAMP),
(23, 13, 15, 1, CURRENT_TIMESTAMP),

-- Pedido 14
(24, 14, 6, 1, CURRENT_TIMESTAMP),

-- Pedido 15
(25, 15, 7, 1, CURRENT_TIMESTAMP),
(26, 15, 5, 2, CURRENT_TIMESTAMP),

-- Pedido 16
(27, 16, 14, 2, CURRENT_TIMESTAMP),
(28, 16, 12, 1, CURRENT_TIMESTAMP),
(29, 16, 3, 1, CURRENT_TIMESTAMP),

-- Pedido 17
(30, 17, 13, 1, CURRENT_TIMESTAMP),
(31, 17, 9, 1, CURRENT_TIMESTAMP),

-- Pedido 18
(32, 18, 8, 2, CURRENT_TIMESTAMP),
(33, 18, 4, 1, CURRENT_TIMESTAMP),

-- Pedido 19
(34, 19, 6, 1, CURRENT_TIMESTAMP),

-- Pedido 20
(35, 20, 14, 2, CURRENT_TIMESTAMP),
(36, 20, 10, 1, CURRENT_TIMESTAMP),

-- Pedido 21
(37, 21, 1, 3, CURRENT_TIMESTAMP),
(38, 21, 11, 1, CURRENT_TIMESTAMP),

-- Pedido 22
(39, 22, 2, 1, CURRENT_TIMESTAMP),

-- Pedido 23
(40, 23, 3, 1, CURRENT_TIMESTAMP),
(41, 23, 8, 2, CURRENT_TIMESTAMP),

-- Pedido 24
(42, 24, 5, 1, CURRENT_TIMESTAMP),

-- Pedido 25
(43, 25, 12, 2, CURRENT_TIMESTAMP),

-- Pedido 26
(44, 26, 7, 1, CURRENT_TIMESTAMP),

-- Pedido 27
(45, 27, 4, 3, CURRENT_TIMESTAMP),
(46, 27, 11, 1, CURRENT_TIMESTAMP),

-- Pedido 28
(47, 28, 15, 1, CURRENT_TIMESTAMP),

-- Pedido 29
(48, 29, 2, 1, CURRENT_TIMESTAMP),
(49, 29, 13, 3, CURRENT_TIMESTAMP),

-- Pedido 30
(50, 30, 9, 2, CURRENT_TIMESTAMP),
(51, 30, 5, 1, CURRENT_TIMESTAMP);


-- =====================================
-- Inserção de dados na tabela TRANSPORTADORAS
-- =====================================
INSERT INTO transportadoras (transportadora_id, nome, criado_em)
VALUES
(1, 'Correios', CURRENT_TIMESTAMP),
(2, 'Transportadora X', CURRENT_TIMESTAMP),
(3, 'Transportadora Y', CURRENT_TIMESTAMP),
(4, 'Rapidão Express', CURRENT_TIMESTAMP),
(5, 'Translogística Brasil', CURRENT_TIMESTAMP);



-- Ajuste de inserção para tabela REMESSAS
INSERT INTO remessas (remessa_id, pedido_id, transportadora_id, codigo_rastreamento, data_envio, data_entrega, status_id, criado_em)
VALUES
(1, 1, 1, 'BR1234567890', '2024-01-01 08:00:00', '2024-01-03 12:30:00', 7, CURRENT_TIMESTAMP), -- entregue
(2, 2, 2, 'XP9876543210', '2024-01-02 09:15:00', '2024-01-04 11:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(3, 3, 3, 'BR1111111111', '2024-01-03 10:00:00', NULL, 6, CURRENT_TIMESTAMP), -- enviado
(4, 4, 4, 'YY2222222222', '2024-01-04 11:30:00', '2024-01-06 14:45:00', 7, CURRENT_TIMESTAMP), -- entregue
(5, 5, 5, 'BR3333333333', '2024-01-05 12:45:00', NULL, 1, CURRENT_TIMESTAMP), -- pendente
(6, 6, 1, 'BR4444444444', '2024-01-06 14:00:00', '2024-01-08 10:30:00', 7, CURRENT_TIMESTAMP), -- entregue
(7, 7, 2, 'XP5555555555', '2024-01-07 15:20:00', '2024-01-09 12:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(8, 8, 3, 'YY6666666666', '2024-01-08 16:30:00', NULL, 6, CURRENT_TIMESTAMP), -- enviado
(9, 9, 4, 'BR7777777777', NULL, NULL, 3, CURRENT_TIMESTAMP), -- cancelado
(10, 10, 5, 'XP8888888888', '2024-01-09 18:00:00', '2024-01-12 10:30:00', 7, CURRENT_TIMESTAMP), -- entregue
(11, 11, 1, 'BR9999999999', '2024-01-10 08:45:00', NULL, 1, CURRENT_TIMESTAMP), -- pendente
(12, 12, 2, 'YY1010101010', '2024-01-11 09:15:00', '2024-01-13 16:20:00', 7, CURRENT_TIMESTAMP), -- entregue
(13, 13, 3, 'BR1212121212', '2024-01-12 10:30:00', '2024-01-14 08:45:00', 7, CURRENT_TIMESTAMP), -- entregue
(14, 14, 4, 'XP1313131313', '2024-01-13 11:00:00', NULL, 1, CURRENT_TIMESTAMP), -- pendente
(15, 15, 5, 'YY1414141414', '2024-01-14 12:15:00', '2024-01-15 14:40:00', 7, CURRENT_TIMESTAMP), -- entregue
(16, 16, 1, 'BR1515151515', '2024-01-15 13:45:00', NULL, 6, CURRENT_TIMESTAMP), -- enviado
(17, 17, 2, 'BR1616161616', '2024-01-16 14:30:00', '2024-01-18 16:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(18, 18, 3, 'XP1717171717', '2024-01-17 15:10:00', '2024-01-19 09:15:00', 7, CURRENT_TIMESTAMP), -- entregue
(19, 19, 4, 'BR1818181818', NULL, NULL, 3, CURRENT_TIMESTAMP), -- cancelado
(20, 20, 5, 'YY1919191919', '2024-01-18 17:30:00', NULL, 6, CURRENT_TIMESTAMP), -- enviado
(21, 21, 1, 'BR2020202020', '2024-01-19 08:00:00', '2024-01-21 12:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(22, 22, 2, 'XP2121212121', '2024-01-20 09:00:00', '2024-01-23 13:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(23, 23, 3, 'YY2323232323', '2024-01-21 10:00:00', NULL, 6, CURRENT_TIMESTAMP), -- enviado
(24, 24, 4, 'BR2424242424', '2024-01-22 11:00:00', '2024-01-25 15:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(25, 25, 5, 'XP2525252525', '2024-01-23 12:00:00', NULL, 1, CURRENT_TIMESTAMP), -- pendente
(26, 26, 1, 'BR2626262626', '2024-01-24 13:00:00', '2024-01-26 10:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(27, 27, 2, 'XP2727272727', '2024-01-25 14:00:00', '2024-01-28 14:00:00', 7, CURRENT_TIMESTAMP), -- entregue
(28, 28, 3, 'YY2828282828', '2024-01-26 15:00:00', NULL, 6, CURRENT_TIMESTAMP), -- enviado
(29, 29, 4, 'BR2929292929', NULL, NULL, 3, CURRENT_TIMESTAMP), -- cancelado
(30, 30, 5, 'XP3030303030', '2024-01-27 16:00:00', NULL, 6, CURRENT_TIMESTAMP); -- enviado

-- Inserção de dados na tabela PAGAMENTOS
INSERT INTO pagamentos (pedido_id, metodo_id, data_pagamento, valor, status_id, criado_em)
SELECT pedido_id, 
       (ARRAY[1, 2, 3, 4, 5])[floor(random() * 5 + 1)],  -- Escolhe um método de pagamento aleatório
       NOW() - INTERVAL '1 day' * floor(random() * 10),  -- Data de pagamento aleatória nos últimos 10 dias
       round((random() * 500 + 50)::numeric, 2),  -- Conversão explícita para numeric antes de arredondar
       (ARRAY[2, 4, 5])[floor(random() * 3 + 1)],  -- Status aleatório: concluído (2), pago (4) ou falhou (5)
       NOW()
FROM pedidos
WHERE pedido_id BETWEEN 1 AND 30
LIMIT 10;

INSERT INTO pagamentos (pedido_id, metodo_id, data_pagamento, valor, status_id, criado_em)
SELECT pedido_id, 
       (ARRAY[1, 2, 3, 4, 5])[floor(random() * 5 + 1)],  
       NOW() - INTERVAL '1 day' * floor(random() * 10),  
       round((random() * 500 + 50)::numeric, 2),  
       (ARRAY[2, 4, 5])[floor(random() * 3 + 1)],  
       NOW()
FROM pedidos
WHERE pedido_id BETWEEN 1 AND 30
LIMIT 10;

INSERT INTO pagamentos (pedido_id, metodo_id, data_pagamento, valor, status_id, criado_em)
SELECT pedido_id, 
       (ARRAY[1, 2, 3, 4, 5])[floor(random() * 5 + 1)],  
       NOW() - INTERVAL '1 day' * floor(random() * 10),  
       round((random() * 500 + 50)::numeric, 2),  
       (ARRAY[2, 4, 5])[floor(random() * 3 + 1)],  
       NOW()
FROM pedidos
WHERE pedido_id BETWEEN 1 AND 30
LIMIT 10;
