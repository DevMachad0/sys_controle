import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('data_sys.db')

# Criar um cursor para executar comandos SQL
cursor = conn.cursor()

# Comandos SQL para criar a tabela 'registro_cliente'
sql_create_table = """
CREATE TABLE registro_venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_venda TEXT,
    codigo TEXT,
    produto TEXT,
    cliente TEXT,
    forma_pagamento TEXT,
    qtd INTEGER,
    desconto REAL,
    valor_total REAL,
    valor_pago REAL
);

"""

# Executar o comando SQL para criar a tabela
cursor.execute(sql_create_table)

# Confirmar as alterações
conn.commit()

# Fechar a conexão com o banco de dados
conn.close()
