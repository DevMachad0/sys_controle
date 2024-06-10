import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt6.QtWidgets import QTableWidgetItem
from Gerenciamento_interface import Ui_Form
import sqlite3
import datetime
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        # Conectar os botões aos métodos correspondentes
        self.ui.Inicio.clicked.connect(self.mostrar_frame_inicio)
        self.ui.produtos.clicked.connect(self.mostrar_frame_produto)
        self.ui.entreda_2.clicked.connect(self.mostrar_frame_entrada)
        self.ui.cadastro_2.clicked.connect(self.mostrar_frame_cadastro)
        self.ui.saida_2.clicked.connect(self.mostrar_frame_saida)
        self.ui.suporte_2.clicked.connect(self.mostrar_frame_suporte)
        # Conectar os botões aos métodos correspondentes
        self.ui.toolButton_3.clicked.connect(self.pesquisar_produto_por_codigo)
        self.ui.pushButton_2.clicked.connect(self.processar_saida)
        self.ui.pushButton_2.clicked.connect(self.cadastrar_saida)
        self.ui.pushButton_5.clicked.connect(self.excluir_item_selecionado_venda)
        self.ui.pushButton_6.clicked.connect(self.aplicar_desconto)
        self.ui.cadastra_cliente.clicked.connect(self.cadastrar_cliente)
        self.ui.castrar_fornecedor.clicked.connect(self.cadastrar_fornecedor)
        self.ui.pushButton_3.clicked.connect(self.adicionar_item_venda)
        self.ui.pushButton_4.clicked.connect(self.registrar_venda)
         # Inicializa os valores dos labels
        self.ui.label_24.setText("Total: R$ 0.00")  # Subtotal
        self.ui.label_25.setText("0.00")            # Desconto
        self.ui.label_28.setText("Total: R$ 0.00")  # Total a Pagar
        # Conectar o botão 'Registrar Produto' ao método correspondente
        self.ui.botao_entreda_salvar.clicked.connect(self.cadastrar_produto)

        # Conexão com o banco de dados SQLite
        self.db_connection = sqlite3.connect("database/data_sys.db")
        self.cursor = self.db_connection.cursor()

        # Carregar fornecedores no QComboBox ao iniciar a aplicação
        self.carregar_fornecedores()
        self.carregar_clientes()

    def mostrar_frame_inicio(self):
        self.ui.stackedWidget.setCurrentIndex(3)
    
    def mostrar_frame_produto(self):
        self.ui.stackedWidget.setCurrentIndex(1)
    
    def mostrar_frame_entrada(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.carregar_fornecedores()  # Certifique-se de carregar os fornecedores ao abrir o frame de entrada
    
    def mostrar_frame_cadastro(self):
        self.ui.stackedWidget.setCurrentIndex(2)
    def mostrar_frame_saida(self):
        self.ui.stackedWidget.setCurrentIndex(4)
    def mostrar_frame_suporte(self):
        self.ui.stackedWidget.setCurrentIndex(5)

    def cadastrar_cliente(self):
        # Coletando os dados do formulário
        codigo = self.ui.codigo_cliente.text()
        nome = self.ui.nome_cliente.text()
        telefone = self.ui.telefone_cliente.text()
        email = self.ui.email_cliente.text()
        cnpj_cpf = self.ui.cnpcpf_cliente.text()
        pessoa = self.ui.pessoa_cliente.currentText()
        endereco = self.ui.endereco_cliente.text()
        cep = self.ui.cep_cliente.text()
        cidade = self.ui.cidade_cliente.text()
        numero = self.ui.numero_cliente.text()
        complemento = self.ui.complemento_cliente.text()

        # Verificando se todos os campos foram preenchidos
        if not (codigo and nome and telefone and cnpj_cpf and pessoa and endereco and cep and cidade and numero):
            QMessageBox.warning(self, "Atenção", "Todos os campos devem ser preenchidos.")
            return

        # Inserindo os dados na tabela registro_cliente
        self.cursor.execute("""
            INSERT INTO registro_cliente 
            (codigo, nome, telefone, email, cnpj_cpf, pessoa, endereco, cep, cidade, numero, complemento) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, nome, telefone, email, cnpj_cpf, pessoa, endereco, cep, cidade, numero, complemento))

        # Commit das alterações
        self.db_connection.commit()

        # Exibir mensagem de sucesso
        QMessageBox.information(self, "Sucesso", "Cadastro de cliente realizado com sucesso.")

        # Limpar os campos após a inserção
        self.limpar_campos()

    def cadastrar_fornecedor(self):
        # Coletando os dados do formulário
        codigo = self.ui.edit_cod_forn.text()
        nome = self.ui.edit_forn_nome.text()
        telefone = self.ui.edit_forn_tele.text()
        email = self.ui.edit_email_.text()
        cnpj_cpf = self.ui.edit_forn_cnpjcpf.text()
        pessoa = self.ui.pessoa_forn.currentText()
        produto_servico = self.ui.prod_edit_forn.text()
        valor = self.ui.valor_edit_forn.text()
        mais_informacao = self.ui.mais_edit_forn.toPlainText()
        endereco = self.ui.ender_edit_forn.text()
        cep = self.ui.cep_edit_forn.text()
        cidade = self.ui.cid_edit_forn.text()
        numero = self.ui.num_edit_forn.text()
        complemento = self.ui.comp_edit_forn.text()

        # Verificando se todos os campos foram preenchidos
        if not (codigo and nome and telefone and cnpj_cpf and pessoa and produto_servico and valor and mais_informacao and endereco and cep and cidade and numero):
            QMessageBox.warning(self, "Atenção", "Todos os campos devem ser preenchidos.")
            return

        # Inserindo os dados na tabela registro_fornecedor
        self.cursor.execute("""
            INSERT INTO registro_fornecedor  
            (codigo, nome, telefone, email, cnpj_cpf, pessoa, produto_servico, valor, mais_informacao, endereco, cep, cidade, numero, complemento) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, nome, telefone, email, cnpj_cpf, pessoa, produto_servico, valor, mais_informacao, endereco, cep, cidade, numero, complemento))

        # Commit das alterações
        self.db_connection.commit()

        # Exibir mensagem de sucesso
        QMessageBox.information(self, "Sucesso", "Cadastro de fornecedor realizado com sucesso.")

        # Limpar os campos após a inserção
        self.limpar_campos()
    def pesquisar_produto_por_codigo(self):
        # Obter o código do produto do lineEdit_7
        codigo_produto = self.ui.lineEdit_7.text()
        
        # Pesquisar no banco de dados
        self.cursor.execute("SELECT * FROM registro_novo_produto WHERE codigo = ?", (codigo_produto,))
        produto = self.cursor.fetchone()
        
        # Verificar se o produto foi encontrado
        if produto:
            # Preencher os lineEdits com as informações do produto encontrado
            self.ui.lineEdit_10.setText(produto[2])  # nome
            self.ui.lineEdit_3.setText(produto[4])   # grupo
            self.ui.volume_atual_saida.setText(str(produto[9]))  # estoque
            self.ui.volume_minimo_saida.setText(str(produto[10]))  # alerta_reposicao
            self.ui.lote_saida.setText(produto[8])  # lote
            self.ui.peso_saida.setText(str(produto[5]))  # peso
            self.ui.medida_saida.setText(str(produto[6]))  # medida
        else:
            QMessageBox.warning(self, "Atenção", "Código não encontrado.")
            # Se o produto não for encontrado, limpar os lineEdits
            self.ui.lineEdit_10.clear()
            self.ui.lineEdit_3.clear()
            self.ui.volume_atual_saida.clear()
            self.ui.volume_minimo_saida.clear()
            self.ui.lote_saida.clear()
    def processar_saida(self):
        # Obter a quantidade de saída do lineEdit_8
        quantidade_saida_str = self.ui.lineEdit_8.text()

        # Verificar se a quantidade de saída é válida
        try:
            quantidade_saida = int(quantidade_saida_str)
        except ValueError:
            QMessageBox.warning(self, "Atenção", "Quantidade inválida.")
            return

        # Obter o estoque atual do banco de dados
        codigo_produto = self.ui.lineEdit_7.text()
        self.cursor.execute("SELECT estoque FROM registro_novo_produto WHERE codigo = ?", (codigo_produto,))
        estoque_atual_str = self.cursor.fetchone()[0]

        try:
            # Convertendo estoque_atual para inteiro
            estoque_atual = int(estoque_atual_str)
        except ValueError:
            QMessageBox.warning(self, "Atenção", "Erro ao obter o estoque atual.")
            return

        # Verificar se há estoque suficiente
        if estoque_atual >= quantidade_saida:
            # Subtrair a quantidade de saída do estoque atual
            estoque_atual -= quantidade_saida

            # Atualizar o estoque no banco de dados
            self.cursor.execute("UPDATE registro_novo_produto SET estoque = ? WHERE codigo = ?", (estoque_atual, codigo_produto))
            self.db_connection.commit()

            QMessageBox.information(self, "Sucesso", f"{quantidade_saida} volumes retirados do estoque.")
            
        else:
            QMessageBox.warning(self, "Atenção", "Estoque insuficiente.")
    def cadastrar_saida(self):
        # Obter os valores dos campos de entrada
        data_saida = datetime.datetime.now().strftime("%Y-%m-%d")  
        codigo = self.ui.lineEdit_7.text()
        produto = self.ui.lineEdit_10.text()
        grupo = self.ui.lineEdit_3.text()
        medida = self.ui.medida_saida.text()
        peso = self.ui.peso_saida.text()
        volume_expedido = self.ui.lineEdit_8.text()
        volume_atual = self.ui.volume_atual_saida.text()
        destino = self.ui.lineEdit_5.text()  # Certifique-se de ter um campo para o destino da saída
        descricao = self.ui.lineEdit_4.text()

        # Verificar se todos os campos obrigatórios foram preenchidos
        if not (codigo and produto and grupo and volume_expedido):
            QMessageBox.warning(self, "Atenção", "Todos os campos (*) devem ser preenchidos.")
            return

        # Inserir os dados na tabela registro_saida
        self.cursor.execute("""
            INSERT INTO registro_saida 
            (codigo, produto, grupo, medida, data_saida, peso, volume_expedido, volume_atual, destino, descricao) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (codigo, produto, grupo, medida, data_saida, peso, volume_expedido, volume_atual, destino, descricao))

        # Commit das alterações
        self.db_connection.commit()

        # Exibir mensagem de sucesso
        QMessageBox.information(self, "Sucesso", "Saída cadastrada com sucesso.")
        self.limpar_campos()

    def cadastrar_produto(self):
        # Coletando os dados do formulário
        codigo = self.ui.codigo.text()
        nome = self.ui.nome.text()
        marca = self.ui.marca.text()
        grupo = self.ui.grupo.text()
        peso = self.ui.peso.text()
        medida = self.ui.medida.text()
        fornecedor = self.ui.fornecedor.currentText()
        lote = self.ui.lote_produto.text()
        estoque = self.ui.estoque.text()
        alerta_reposicao = self.ui.reposicao.text()
        valor_venda = self.ui.venda.text()
        valor_compra = self.ui.lineEdit_2.text()
        descricao = self.ui.descricao.text()

        # Verificando se todos os campos foram preenchidos
        if not (codigo and nome and marca and grupo and peso and medida and fornecedor and lote and estoque and alerta_reposicao and valor_venda and valor_compra and descricao):
            QMessageBox.warning(self, "Atenção", "Todos os campos devem ser preenchidos.")
            return

        # Inserindo os dados na tabela registro_novo_produto
        self.cursor.execute("""
                    INSERT INTO registro_novo_produto 
                    (codigo, nome, marca, grupo, peso, medida, fornecedor, lote, estoque,alerta_reposicao , valor_venda, valor_compra, descricao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (codigo, nome, marca, grupo, peso, medida, fornecedor, lote, estoque, alerta_reposicao, valor_venda, valor_compra, descricao))
        # Commit das alterações
        self.db_connection.commit()
                # Limpar os campos após a inserção
        self.limpar_campos()
    
        # Exibir mensagem de sucesso
        QMessageBox.information(self, "Sucesso", "Cadastro de produto realizado com sucesso.")

    def carregar_fornecedores(self):
        self.cursor.execute("SELECT nome FROM registro_fornecedor")
        fornecedores = self.cursor.fetchall()
        
        self.ui.fornecedor.clear()
        for fornecedor in fornecedores:
            self.ui.fornecedor.addItem(fornecedor[0])
    def carregar_clientes(self):
        self.cursor.execute("SELECT nome FROM registro_cliente")
        clientes = self.cursor.fetchall()
        
        self.ui.comboBox_3.clear()
        for cliente in clientes:
            self.ui.comboBox_3.addItem(cliente[0])

    def adicionar_item_venda(self):
        codigo_produto = self.ui.lineEdit_6.text()  # Mudança para lineEdit_7
        quantidade_expedida = self.ui.lineEdit_9.text()
        # Verifica se a quantidade expedida é válida
        if not quantidade_expedida.isdigit():
            QMessageBox.warning(self, "Erro", "Quantidade expedida inválida.")
            return
        quantidade_expedida = int(quantidade_expedida)  # Converte para inteiro após a verificação

        # Verifica se o código do produto está preenchido
        if not codigo_produto:
            QMessageBox.warning(self, "Erro", "Por favor, insira o código do produto.")
            return

        # Consulta o banco de dados para verificar se o produto existe
        self.cursor.execute("SELECT nome, estoque, valor_venda FROM registro_novo_produto WHERE codigo = ?", (codigo_produto,))
        produto = self.cursor.fetchone()

        if not produto:
            QMessageBox.warning(self, "Erro", "Produto não encontrado.")
            return

        nome_produto, estoque, valor_unitario = produto
        estoque = int(estoque)  # Converte para inteiro
        valor_unitario = float(valor_unitario)  # Converte para float

        # Verifica se a quantidade em estoque é suficiente
        if quantidade_expedida > estoque:
            QMessageBox.warning(self, "Erro", "Quantidade expedida maior que o estoque disponível.")
            return

        # Calcula o valor total
        valor_total = quantidade_expedida * valor_unitario

        # Adiciona o item ao carrinho (tabela)
        row_position = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(row_position)
        self.ui.tableWidget.setItem(row_position, 0, QTableWidgetItem(str(quantidade_expedida)))
        self.ui.tableWidget.setItem(row_position, 1, QTableWidgetItem(nome_produto))
        self.ui.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(estoque)))
        self.ui.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(valor_unitario)))
        self.ui.tableWidget.setItem(row_position, 4, QTableWidgetItem(str(valor_total)))
        self.atualizar_total()
    def atualizar_total(self):
        total = 0.0
        for row in range(self.ui.tableWidget.rowCount()):
            valor_total_item = self.ui.tableWidget.item(row, 4).text()
            total += float(valor_total_item)
        
        self.ui.label_24.setText(f"Total: R$ {total:.2f}")
                # Atualiza o total a pagar (label_28) inicialmente com o subtotal
        self.ui.label_28.setText(f"Total: R$ {total:.2f}")
    def excluir_item_selecionado_venda(self):
        # Obter as linhas selecionadas
        linhas_selecionadas = self.ui.tableWidget.selectionModel().selectedRows()
        
        # Verificar se alguma linha foi selecionada
        if linhas_selecionadas:
            # Iterar sobre as linhas selecionadas em ordem reversa para evitar problemas de índice
            for linha in sorted(linhas_selecionadas, reverse=True):
                self.ui.tableWidget.removeRow(linha.row())
                self.atualizar_total()
        else:
            QMessageBox.warning(self, "Atenção", "Nenhuma linha selecionada para excluir.")

    def aplicar_desconto(self):
        desconto = self.ui.lineEdit_12.text()

        # Verifica se o desconto é válido
        if not desconto.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Erro", "Desconto inválido.")
            return

        desconto = float(desconto)

        # Extrair o subtotal do label_24, removendo a parte do texto
        subtotal_text = self.ui.label_24.text().replace('Total: R$ ', '')
        subtotal = float(subtotal_text)
        
        total_com_desconto = subtotal - desconto

        # Atualiza o label_25 e label_28 com os novos valores
        self.ui.label_25.setText(f"{desconto:.2f}")
        self.ui.label_28.setText(f"Total: R$ {total_com_desconto:.2f}")

    def registrar_venda(self):
        cliente = self.ui.comboBox_3.currentText()
        forma_pagamento = self.ui.comboBox_2.currentText()
        desconto = self.ui.lineEdit_12.text()
        valor_total = float(self.ui.label_28.text().split("R$")[1].strip())
        valor_pago = self.ui.lineEdit_11.text()
        
        if not desconto.isdigit():
            desconto = 0
        else:
            desconto = float(desconto)

        if not valor_pago.replace('.', '', 1).isdigit():
            QMessageBox.warning(self, "Erro", "Valor pago inválido.")
            return

        valor_pago = float(valor_pago)

        if valor_pago < valor_total:
            QMessageBox.warning(self, "Erro", "Valor pago é inferior ao valor total a pagar.")
            return

        troco = valor_pago - valor_total if valor_pago > valor_total else 0

        data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Inserir informações de cada item no banco de dados
        for row in range(self.ui.tableWidget.rowCount()):
            qtd = self.ui.tableWidget.item(row, 0).text()
            produto = self.ui.tableWidget.item(row, 1).text()
            codigo = self.ui.lineEdit_6.text()
            self.cursor.execute("""
                INSERT INTO registro_venda (qtd, codigo, produto, cliente, forma_pagamento, data_venda, desconto, valor_total, valor_pago, troco)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (qtd, codigo, produto, cliente, forma_pagamento, data_venda, desconto, valor_total, valor_pago, troco))

        self.db_connection.commit()
        
        if troco > 0:
            QMessageBox.information(self, "Venda registrada com sucesso", f"Venda registrada com sucesso. Troco: R$ {troco:.2f}")
        else:
            QMessageBox.information(self, "Sucesso", "Venda registrada com sucesso.")

        # Limpar tabela e campos após registrar a venda
        self.ui.tableWidget.setRowCount(0)
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_9.clear()
        self.ui.lineEdit_12.clear()
        self.ui.lineEdit_11.clear()
        self.ui.label_24.setText("Total: R$ 0.00")
        self.ui.label_25.setText("Desconto: R$ 0.00")
        self.ui.label_28.setText("Total a Pagar: R$ 0.00")
    def limpar_campos(self):
        # Limpar apenas o texto dos campos QLineEdit de cliente
        self.ui.codigo_cliente.clear()
        self.ui.nome_cliente.clear()
        self.ui.telefone_cliente.clear()
        self.ui.email_cliente.clear()
        self.ui.cnpcpf_cliente.clear()
        self.ui.endereco_cliente.clear()
        self.ui.cep_cliente.clear()
        self.ui.cidade_cliente.clear()
        self.ui.numero_cliente.clear()
        self.ui.complemento_cliente.clear()

        # Limpar apenas o texto dos campos QLineEdit de fornecedor
        self.ui.edit_cod_forn.clear()
        self.ui.edit_forn_nome.clear()
        self.ui.edit_forn_tele.clear()
        self.ui.edit_email_.clear()
        self.ui.edit_forn_cnpjcpf.clear()
        self.ui.prod_edit_forn.clear()
        self.ui.valor_edit_forn.clear()
        self.ui.mais_edit_forn.clear()
        self.ui.ender_edit_forn.clear()
        self.ui.cep_edit_forn.clear()
        self.ui.cid_edit_forn.clear()
        self.ui.num_edit_forn.clear()
        self.ui.comp_edit_forn.clear()

        # Limpar apenas o texto dos campos QLineEdit de produto
        self.ui.codigo.clear()
        self.ui.nome.clear()
        self.ui.marca.clear()
        self.ui.grupo.clear()
        self.ui.peso.clear()
        self.ui.medida.clear()
        self.ui.estoque.clear()
        self.ui.lote_produto.clear()
        self.ui.reposicao.clear()
        self.ui.venda.clear()
        self.ui.lineEdit_2.clear()
        self.ui.descricao.clear()
        #limpar saida de produtos
        self.ui.lineEdit_8.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_4.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
