Descrição
Este projeto é um sistema de controle de estoque e registro de vendas desenvolvido em Python utilizando PyQt5 para a interface gráfica e SQLite para o banco de dados. O objetivo do sistema é facilitar o gerenciamento de produtos em estoque, registrar saídas de produtos e realizar vendas, mantendo um registro detalhado de todas as transações.

Funcionalidades
Controle de Estoque
Cadastro de Produtos: Permite o cadastro de novos produtos no sistema, incluindo informações como código, nome, grupo, unidade de medida, quantidade em estoque, peso, volume e descrição.
Atualização de Estoque: Permite a atualização do estoque dos produtos existentes.
Registro de Saídas: Registra a saída de produtos do estoque, atualizando automaticamente a quantidade em estoque após a saída ser confirmada.
Registro de Vendas
Adicionar Produtos à Venda: Permite adicionar produtos a uma venda atual, inserindo a quantidade expedida e exibindo o nome do produto, estoque disponível, valor unitário e valor total na tabela de itens da venda.
Calcular Subtotal: Atualiza o subtotal da venda automaticamente ao adicionar produtos à venda.
Aplicar Desconto: Permite aplicar um desconto ao valor total da venda, exibindo o valor do desconto e o valor total a pagar após o desconto.
Registro de Vendas: Registra a venda no banco de dados, salvando informações como cliente, forma de pagamento, data da venda, desconto, valor total, valor pago e troco.
Troco: Calcula e exibe o troco quando o valor pago é maior que o valor total a pagar.
Gerenciamento de Clientes
Cadastro de Clientes: Permite o cadastro de clientes no sistema, incluindo informações relevantes para a realização de vendas.
Seleção de Cliente: Permite a seleção de um cliente para a venda atual a partir de uma lista de clientes cadastrados.


